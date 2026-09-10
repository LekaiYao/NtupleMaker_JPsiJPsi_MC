# MC NtupleMaker

main 共用一套 C++ 物理操作，通过配置选择 2016preVFP、2016postVFP 或 2018，以及 SPS 或 DPS。CRAB 提交脚本由各项目的 new_MC_manager 或人工单独维护。

## 常用命令

```bash
cmssw-el7
cd /afs/cern.ch/user/l/leyao/work/26JJ/v2_crab_MC_Maker/ULPythia2016postVFP/CMSSW_10_6_20/src
cmsenv
scram b -j 2
cd NtupleMaker/NtupleMaker/test
cmsRun BPH_NtupleMaker.py era=2016postVFP channel=DPS
```

默认参数来自 `NtupleMaker/python/year_config.py`，目前为 2016postVFP、DPS。命令行可以覆盖年份、通道、输入、输出和事件数。使用本项目已有 SPS 输入的示例：

```bash
cmsRun BPH_NtupleMaker.py era=2016postVFP channel=SPS \
  inputFiles=file:/eos/home-l/leyao/26JJ/v2_crab_MC_Maker/ULPythia2016postVFP/config_archive/previous_layout_20260909/CMSSW_10_6_20/src/BPH-RECOMINIAOD-MERGED-SPS_13TeV.root \
  outputFile=Ntuple_2016postVFP_SPS.root
```

2018 使用相同入口：

```bash
cmsRun BPH_NtupleMaker.py era=2018 channel=SPS \
  inputFiles=file:/eos/home-l/leyao/26JJ/v2_crab_MC_Maker/ULPythia2018/CMSSW_10_6_20/src/BPH-RECOMINIAOD-SPS_13TeV.root \
  outputFile=Ntuple_2018_SPS.root
```

默认输入为相对 test 目录的 `../../../BPH-RECOMINIAOD-通道_13TeV.root`，默认输出为 `BPH-NTUPLE-通道_13TeV.root`，单线程、读取全部事件。输出文件名不用于判断年份或通道，多个年份共用目录时应显式指定不同输出名。

## 配置与共用操作

| 配置层 | 职责 |
| --- | --- |
| year_config.py | 默认年份、默认通道、各年份 GlobalTag、触发路径和三个 filter |
| NtupleMaker_cfi.py | 共用输入标签、makeNtuple(era, channel)、SPS/DPS 同母粒子条件 |
| BPH_NtupleMaker.py | 共用运行流程，解析参数并同时选择 GlobalTag 与分析器配置 |
| NtupleMaker.cc | 共用真值配对、muon 选择、顶点拟合、触发匹配和 samePV |

不支持的年份或通道会在加载时明确报错。2017 尚未添加预设。2016preVFP 复用 postVFP 的触发参数，GlobalTag 为 106X_mcRun2_asymptotic_preVFP_v9。原 rootupleSPS/rootupleDPS 仍指向 2016postVFP；rootuple2018SPS/rootuple2018DPS 也保留。

SPS 使用 requireSameMother=True，DPS 使用 False；这仍是既有真值配对条件，不等同于严格的硬散射来源定义。母粒子空指针保护保留，硬散射来源等物理待办见 [真值配对记录](docs/truth_pairing_pending.md)。

输入为 `slimmedMuons::RECO`、`packedPFCandidates::RECO` 和 `TriggerResults::HLT`，对应合并生产输出。ROOT 记录 era、channel、requireSameMother 及完整分析器配置。

## 分支与生产维护

- main：2016preVFP、2016postVFP 和 2018 共用代码，物理操作只维护一次。
- v2_ULPythia2016postVFP：年份整合前 main 的备份，提交 fd3a787。
- v2_ULPythia2018：原来单独验证的 2018 版本。

仓库必须位于 `CMSSW/src/NtupleMaker`，保留内层 NtupleMaker 包。不同工作目录分别更新到选定 commit 或 tag、编译和验证；固定生产批次的代码版本，不能将一个目录更新等同于所有环境已更新。

CRAB 提交脚本由管理器或人工单独维护。各生产目录须在 year_config.py 选择对应 DEFAULT_ERA 并保留 DEFAULT_CHANNEL=DPS；也可显式传入 pyCfgParams（例如 era=2018、channel=DPS）。入口不会根据任务名自动识别年份。

原始代码来自 chensh 的 2016 DPS NtupleMaker；2018 标签按官方 2018v32 菜单核验，保留此前对 L1 与顶点 filter 对调的修正。基线校验清单 `docs/baseline_sha256.json` 记录的是原始建仓库版本。

## 回归验证

在 2016 CMSSW_10_6_20 环境用统一 main 读取合并前相同的 SPS MiniAOD，按事件标识对齐并比较全部物理树分支。2016 和 2018、SPS 和 DPS 四组合的输出与各自原结果比较；输入均为 SPS，小样本回归不能代替真实 DPS 物理验证。

原始报告与运行日志保存在项目 `config_archive/tests/year_unification_20260910/`。四组合均通过全 84 分支对比，具体差异和适用范围见 [年份整合回归记录](docs/year_unification_regression.md)。

2016preVFP 新增预设及四步测试结果见 [preVFP 验证记录](docs/preVFP_validation.md)，其中记录了沿用 L1 辅助分支的已知限制。
