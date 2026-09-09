# MC NtupleMaker

用于 J/ψ 对 MC 的 Ntuple 制作。当前基线为 UL2016postVFP，共用 C++ 实现并提供 SPS/DPS 配置；运行入口当前选择 DPS。

## 常用命令

进入现有环境编译：

```bash
cmssw-el7
cd /afs/cern.ch/user/l/leyao/work/26JJ/v2_crab_MC_Maker/ULPythia2016postVFP/CMSSW_10_6_20/src
cmsenv
scram b -j 2
cd NtupleMaker/NtupleMaker/test
cmsRun BPH_NtupleMaker.py
```

运行前准备 `CMSSW_10_6_20/src/BPH-RECOMINIAOD-DPS_13TeV.root`，或修改运行配置中的输入路径。当前示例使用 1 个线程，读取全部事件，输出 `BPH-NTUPLE-DPS_13TeV.root`。建仓库本身没有重新执行事件处理。

CRAB 提交示例位于同一 test 目录：

```bash
source /cvmfs/cms.cern.ch/crab3/crab.sh prod
crab submit -c crab_NTUPLE_DPS.py
```

提交前填写真实 `inputDataset`，检查任务名、输出目录及站点；仓库中的脚本保留本项目设置。

## 通道配置

`NtupleMaker/python/NtupleMaker_cfi.py` 提供 `rootupleSPS` 和 `rootupleDPS`。在 `NtupleMaker/test/BPH_NtupleMaker.py` 导入所需预设并 clone，切换时同时检查输入、输出名称。无需修改 C++。

| 预设 | channel | requireSameMother |
| --- | --- | --- |
| rootupleSPS | SPS | True |
| rootupleDPS | DPS | False |

同母粒子条件是保留的样本配对规则，不能替代硬散射来源判定。真值母粒子访问已有空指针保护；详细待办见 [真值配对待办](docs/truth_pairing_pending.md)。ROOT 保存通道和配置信息。

当前输入使用 `slimmedMuons::RECO`、`packedPFCandidates::RECO` 和 `TriggerResults::HLT`，对应合并生产输出。GlobalTag 为 `106X_mcRun2_asymptotic_v13`。

## 仓库布局与安装

仓库根目录必须放在 `CMSSW/src/NtupleMaker`，保留内层 `NtupleMaker` 包目录：

```text
NtupleMaker/                 ← Git 仓库根目录
  NtupleMaker/
    BuildFile.xml
    src/NtupleMaker.cc
    python/NtupleMaker_cfi.py
    test/BPH_NtupleMaker.py
    test/crab_NTUPLE_DPS.py
  docs/
```

在另一个 CMSSW 环境的 src 下，使用 `git clone <仓库地址> NtupleMaker` 安装，再进入 cmssw-el7、初始化 cmsenv 并编译。不要压平两层目录，否则现有 Python 导入路径会改变。ROOT、日志、CRAB 工作目录及 Python 缓存不纳入 Git。

## 多年份共用方案

合并为负责 SPS/DPS、2016–2018 的仓库可行。保留共享 C++，将年份和通道作为独立配置维度；后续把目前 C++ 中的触发 filter 字符串移到年份配置，分别提供 2016preVFP、2016postVFP、2017、2018 的 GlobalTag、触发路径与输入标签预设。

当前仅整理现有版本，尚未实现上述多年份预设。2018 参考源码与 2016 的主要差异为三个触发 filter 字符串；其与 L1、L3、顶点匹配的对应关系需要核验后再迁入。输入 process 名应按实际 MiniAOD 内容配置，不能仅凭年份推断。

现有软件验证使用同一份 31 事件 SPS MiniAOD，SPS/DPS 两种预设均运行成功，SPS 输出与参数化前一致。这不代表真实 DPS 样本或其他年份已经验证；各年份、通道仍需代表性输入回归测试。

## 来源与远端

原始来源为 chensh 的 2016 DPS NtupleMaker：
`/eos/user/c/chensh/JPsiJPsi/SKIM_tightfilter/DPS/ULPythia2016/CMSSW_10_6_20/src/NtupleMaker/`。

本项目增加母粒子空指针保护、通道参数和输出配置记录，并适配当前合并生产的输入。建仓库前代码校验值记录在 [基线清单](docs/baseline_sha256.json)。未擅自指定原始代码的许可证。

本地仓库使用 main 分支。远端地址尚未指定；创建空远端后，在仓库根目录执行：

```bash
git remote add origin <仓库地址>
git push -u origin main
```

远端仓库名与可见性由维护者选择；若计划公开分发，应先与原作者确认授权及许可证。
