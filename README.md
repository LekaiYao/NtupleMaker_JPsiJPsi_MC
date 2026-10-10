# v3 DPS MC ntuple 生产

支持 `2016preVFP / 2016postVFP / 2017 / 2018`，流程为 `GENSIMDIGI → HLT → RECOMINIAOD → NTUPLE`。需要 CMS grid 证书、CRAB 权限及可写存储站点。以下在同一个 EL7 Bash 会话执行；CERN 先进入 `cmssw-el7`。

## 1. 从空目录建立环境

修改年份、CMS 用户名和存储站点；每个年份使用独立目录，每个生产批次使用新 `MC_SET`。

```bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export MC_ERA=2017                    # 2016preVFP / 2016postVFP / 2017 / 2018
export CRAB_USER=your_cms_username    # 自己的 CMS 用户名
export CRAB_SITE=T2_FR_IPHC           # 自己有写权限的站点
export MC_SET=v3_set1
mkdir "MC_${MC_ERA}" && cd "MC_${MC_ERA}"
export MC_WORK="$PWD"
git clone --branch v3_fiducial https://github.com/LekaiYao/NtupleMaker_JPsiJPsi_MC.git recipe
source recipe/production/era.sh "$MC_ERA"
SCRAM_ARCH="$MAIN_ARCH" scram project CMSSW "$MAIN_RELEASE"
SCRAM_ARCH="$HLT_ARCH" scram project CMSSW "$HLT_RELEASE"
mv recipe "$MAIN_RELEASE/src/NtupleMaker"
export RECIPE="$MC_WORK/$MAIN_RELEASE/src/NtupleMaker/production"
mkdir -p "$MAIN_RELEASE/src/Configuration/GenProduction/python"
cp "$RECIPE/Fragment_DPStoJJ_Direct_2018.py" "$MAIN_RELEASE/src/Configuration/GenProduction/python/"
source "$RECIPE/workflow.sh"
in_release "$MAIN_RELEASE" "$MAIN_ARCH" scram b -j 2
source /cvmfs/cms.cern.ch/crab3/crab.sh prod
voms-proxy-init --voms cms --valid 192:00
```

## 2. 生成生产 PSet

年份脚本已选择对应 CMSSW、GlobalTag、HLT 菜单、beamspot 和 premix。以下命令只生成配置；NTUPLE 直接使用仓库的 `BPH_NtupleMaker.py`。

```bash
in_release "$MAIN_RELEASE" "$MAIN_ARCH" python "$RECIPE/load_premix.py" "$MC_ERA" > "$RECIPE/premix/${PREMIX_KEY}.txt"

in_release "$MAIN_RELEASE" "$MAIN_ARCH" cmsDriver.py Configuration/GenProduction/python/Fragment_DPStoJJ_Direct_2018.py \
  --fileout file:BPH-GENSIMDIGI-DPS_13TeV.root --pileup_input "filelist:$RECIPE/premix/${PREMIX_KEY}.txt" \
  --mc --eventcontent PREMIXRAW --runUnscheduled --datatier GEN-SIM-DIGI --conditions "$MC_GT" \
  --step GEN,SIM,DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --nThreads 2 \
  --geometry DB:Extended --datamix PreMix --era "$MC_CMSSW_ERA" --beamspot "$BEAMSPOT" \
  --python_filename BPH_GENSIMDIGI_DPS_13TeV_cfg.py -n 1000 --no_exec \
  --customise_commands "import os, imp; process = imp.load_source('jj_premix', os.path.join(os.environ['CMSSW_BASE'], 'src', 'NtupleMaker', 'production', 'load_premix.py')).customise(process, '$MC_ERA'); process.MessageLogger.cerr.FwkReport.reportEvery=100; process.options.wantSummary=cms.untracked.bool(True)"
in_release "$MAIN_RELEASE" "$MAIN_ARCH" python "$RECIPE/compact_GENSIMDIGI_cfg.py" BPH_GENSIMDIGI_DPS_13TeV_cfg.py

in_release "$HLT_RELEASE" "$HLT_ARCH" cmsDriver.py step4 \
  --filein "file:../../$MAIN_RELEASE/src/BPH-GENSIMDIGI-DPS_13TeV.root" --fileout file:BPH-HLT-DPS_13TeV.root \
  --mc --eventcontent RAWSIM --datatier GEN-SIM-RAW --conditions "$HLT_GT" \
  --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' \
  --step "HLT:$HLT_MENU" --nThreads 2 --geometry DB:Extended --era "$HLT_ERA" "${HLT_KEEP_ARGS[@]}" \
  --python_filename BPH_HLT_DPS_13TeV_cfg.py -n 1000 --no_exec

in_release "$MAIN_RELEASE" "$MAIN_ARCH" cmsDriver.py step5 \
  --filein "file:../../$HLT_RELEASE/src/BPH-HLT-DPS_13TeV.root" --fileout file:BPH-RECOMINIAOD-DPS_13TeV.root \
  --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions "$MC_GT" \
  --step RAW2DIGI,L1Reco,RECO,RECOSIM,PAT --nThreads 2 --geometry DB:Extended --era "$MC_CMSSW_ERA" \
  --python_filename BPH_RECOMINIAOD_DPS_13TeV_cfg.py -n 1000 --no_exec
```

## 3. 依次提交四步

首步默认 10⁹ events、100000 events/job；按需修改下面两个参数。前三步发布到 DBS，NTUPLE 不发布。输出目录为 `/store/user/<用户名>/JJMC/UL<年份>/DPS/<步骤>`。

```bash
make_config GENSIMDIGI --events 1000000000 --events-per-job 100000
crab_step GENSIMDIGI submit
crab_step GENSIMDIGI status
```

等待 GENSIMDIGI 作业及 publication 完成，从其 `status` 输出复制真实 `Output dataset`：

```bash
read -r -p 'GENSIMDIGI Output dataset: ' DATASET
make_config HLT --input "$DATASET"
crab_step HLT submit
crab_step HLT status
```

等待 HLT 作业及 publication 完成：

```bash
read -r -p 'HLT Output dataset: ' DATASET
make_config RECOMINIAOD --input "$DATASET"
crab_step RECOMINIAOD submit
crab_step RECOMINIAOD status
```

等待 RECOMINIAOD 作业及 publication 完成：

```bash
read -r -p 'RECOMINIAOD Output dataset: ' DATASET
make_config NTUPLE --input "$DATASET"
crab_step NTUPLE submit
crab_step NTUPLE status
```

NTUPLE 完成后获取 ROOT 文件访问地址：

```bash
crab_step NTUPLE getoutput
```

树为 `rootuple/oniaTree`；元数据 `rootuple/selectionVersion`、`rootuple/era`、`rootuple/channel` 应分别为 `v3_fiducial`、所选年份、`DPS`。已有 MiniAOD 时，完成第 1 节后可直接生成并提交 NTUPLE。
