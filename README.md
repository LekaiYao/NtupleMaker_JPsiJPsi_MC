# MC NtupleMaker

从已有的 MC MiniAOD 生成 J/ψ 对 ntuple，支持 2016preVFP、2016postVFP、2017、2018 的 SPS 和 DPS。以下使用本轮生产的 `v3_fiducial` 分支；不涉及 MiniAOD 的生成步骤。

## 安装

四个年份均使用 **CMSSW_10_6_20**，架构为 **slc7_amd64_gcc700**。在 lxplus 上先进入 EL7 环境，再建立工作区：

```bash
cmssw-el7
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_20
cd CMSSW_10_6_20/src
cmsenv
git clone --branch v3_fiducial https://github.com/LekaiYao/NtupleMaker_JPsiJPsi_MC.git NtupleMaker
scram b -j 2
```

已有相同 CMSSW 环境时，从对应的 `src` 目录执行 `cmsenv`，然后克隆、编译即可。保留仓库内外两层 `NtupleMaker` 目录。

## 年份与通道

运行入口是 `NtupleMaker/NtupleMaker/test/BPH_NtupleMaker.py`（相对于 CMSSW 的 `src`）。通过 `era` 和 `channel` 选择样本，程序自动设置 GlobalTag 和触发配置，无需修改 C++。

| `era` | NtupleMaker 使用的 GlobalTag |
| --- | --- |
| `2016preVFP` | `106X_mcRun2_asymptotic_preVFP_v9` |
| `2016postVFP` | `106X_mcRun2_asymptotic_v13` |
| `2017` | `106X_mc2017_realistic_v8` |
| `2018` | `106X_upgrade2018_realistic_v15_L1v1` |

`channel` 可选 `SPS` 或 `DPS`，分别启用或关闭真值配对的同母粒子要求。年份与触发设置集中在 [year_config.py](NtupleMaker/python/year_config.py)；2016pre/post 共用触发设置，2017/2018 共用触发设置。

## 接入现有 CRAB 配置

沿用自己的 MiniAOD 数据集、任务名称、输出目录和存储站点。在 **CMSSW 的 `src` 目录提交**，将 ntuple 任务的相关字段设置为：

```python
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'NtupleMaker/NtupleMaker/test/BPH_NtupleMaker.py'
config.JobType.pyCfgParams = ['era=2017', 'channel=DPS']
config.JobType.numCores = 1
config.JobType.maxMemoryMB = 2000
config.JobType.allowUndistributedCMSSW = True
config.Data.publication = False
```

把示例中的 `2017`、`DPS` 改为本次样本。输入由现有 CRAB 配置的 `Data.inputDataset` 指定；私有生产的 `/USER` 数据集使用 `Data.inputDBS = 'phys03'`。建议每个任务显式传入年份和通道，避免依赖本地默认值。

默认输出为 `BPH-NTUPLE-DPS_13TeV.root`（SPS 对应 `BPH-NTUPLE-SPS_13TeV.root`），树为 `rootuple/oniaTree`。文件中的 `rootuple/selectionVersion` 应为 `v3_fiducial`，`rootuple/era` 和 `rootuple/channel` 记录本次配置。
