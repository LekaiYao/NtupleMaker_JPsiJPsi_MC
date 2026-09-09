# MC NtupleMaker

用于 J/ψ 对 MC 的 Ntuple 制作。当前分支 `v2_ULPythia2018` 提供 2018 SPS/DPS 配置，保留 2016 预设，共用 C++ 实现。

## 常用命令

```bash
cmssw-el7
cd /afs/cern.ch/user/l/leyao/work/26JJ/v2_crab_MC_Maker/ULPythia2018/CMSSW_10_6_20/src
cmsenv
scram b -j 2
cd NtupleMaker/NtupleMaker/test
cmsRun BPH_NtupleMaker_SPS.py
```

SPS 输入为 src 下的 `BPH-RECOMINIAOD-SPS_13TeV.root`，输出为当前 test 目录的 `BPH-NTUPLE-SPS_13TeV.root`。DPS 入口为 `BPH_NtupleMaker.py`，输入与输出采用 DPS 名称。两个入口均为 1 线程，读取全部事件。

DPS CRAB 提交在同一 test 目录执行，先填写真实 inputDataset，检查任务名、输出位置和站点：

```bash
source /cvmfs/cms.cern.ch/crab3/crab.sh prod
crab submit -c crab_NTUPLE_DPS.py
```

## 年份和通道配置

`NtupleMaker/python/NtupleMaker_cfi.py` 定义以下预设。切换时在运行配置导入相应预设并 clone，同时检查 GlobalTag、输入和输出文件名。

| 预设 | 年份 | channel | requireSameMother |
| --- | --- | --- | --- |
| rootupleSPS | 2016postVFP | SPS | True |
| rootupleDPS | 2016postVFP | DPS | False |
| rootuple2018SPS | 2018 | SPS | True |
| rootuple2018DPS | 2018 | DPS | False |

2018 使用 `106X_upgrade2018_realistic_v15_L1v1`；输入采用 `slimmedMuons::RECO`、`packedPFCandidates::RECO`、`TriggerResults::HLT`。

触发路径和 L1、L3、顶点 filter 均由 Python 配置，C++ 不再按年份硬编码。2018 对应 `HLT:2018v32`；修正了参考源码将 L1 与顶点 filter 对调的问题，详见 [触发核验](docs/2018_trigger_audit.md)。ROOT 保存 era、channel、requireSameMother 和完整分析器配置。

母粒子空指针保护与同母粒子条件保持原有实现。SPS/DPS 参数只控制既有配对条件，不证明硬散射来源；[真值待办](docs/truth_pairing_pending.md)仍未实施。2017 和 2016preVFP 尚无独立预设。

## 仓库布局

仓库根放在 `CMSSW/src/NtupleMaker`，保留内层 `NtupleMaker` 包，以维持 `NtupleMaker.NtupleMaker` 导入路径。

```bash
# 在另一个 CMSSW 的 src 目录执行
git clone -b v2_ULPythia2018 https://github.com/LekaiYao/NtupleMaker_JPsiJPsi_MC.git NtupleMaker
```

ROOT、日志、CRAB 工作目录、Python 缓存不纳入 Git。

## 来源与验证

基线来自本仓库 main 分支 `fd3a787`，原始代码来源为 chensh 2016 DPS NtupleMaker；2018 参考目录为 `/eos/user/c/chensh/JPsiJPsi/SKIM_tightfilter/DPS/ULPythia2018/CMSSW_10_6_20/src/NtupleMaker/`。`docs/baseline_sha256.json` 是原始 2016 建仓库快照，不是当前分支校验清单。

2018 已完成编译、配置加载、CRAB 序列化及 SPS 四步事件测试。1000 个生成事件中 28 个通过原过滤，三个 EDM 步骤和两种 Ntuple 预设均保留这 28 个事件；目标 HLT 通过 17 个事件，Ntuple 中 4 个事件通过触发匹配。两种预设都使用 SPS 输入，不构成 DPS 物理验证。结果见 [触发核验](docs/2018_trigger_audit.md) 和项目 `config_archive/tests/SPS/`。未提交 CRAB 生产任务。
