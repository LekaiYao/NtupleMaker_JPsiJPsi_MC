# MC NtupleMaker

在 `CMSSW_10_6_20` 中读取 MC MiniAOD，生成 J/ψ 对的 Ntuple。支持 `2016preVFP`、`2016postVFP`、`2017`、`2018`，以及 `SPS`、`DPS` 两种通道。

## 1. 安装与编译

在已有 CMSSW 环境的上一级目录执行：

```bash
cmssw-el7
cd CMSSW_10_6_20/src
cmsenv
git clone https://github.com/LekaiYao/NtupleMaker_JPsiJPsi_MC.git NtupleMaker
scram b -j 2
cd NtupleMaker/NtupleMaker/test
```

仓库放在 `CMSSW_10_6_20/src/NtupleMaker`，保留仓库内层的 `NtupleMaker` 包。

## 2. 切换年份与通道

相对于仓库根目录，修改 `NtupleMaker/python/year_config.py` 中的两项：

```python
DEFAULT_ERA = '2016postVFP'
DEFAULT_CHANNEL = 'DPS'
```

| 参数 | 可选值 | 自动选择的配置 |
| --- | --- | --- |
| `DEFAULT_ERA` | `2016preVFP`、`2016postVFP`、`2017`、`2018` | GlobalTag、触发路径和 filter |
| `DEFAULT_CHANNEL` | `SPS`、`DPS` | 真值配对的同母粒子要求及默认输入输出文件名 |

`SPS` 对应 `requireSameMother=True`，`DPS` 对应 `False`。2016preVFP 与 2016postVFP 共用触发设置，使用各自的 GlobalTag。2017 与 2018 共用触发设置，使用各自的 GlobalTag。

切换年份或通道只需修改上述配置，无需修改 `NtupleMaker.cc`。单次运行也可使用命令行参数覆盖默认值：

```bash
cmsRun BPH_NtupleMaker.py era=2016preVFP channel=DPS
cmsRun BPH_NtupleMaker.py era=2016postVFP channel=SPS
cmsRun BPH_NtupleMaker.py era=2018 channel=DPS
```

## 3. 输入输出与运行

以下命令在 `NtupleMaker/NtupleMaker/test` 目录执行，使用配置中的默认年份和通道：

```bash
cmsRun BPH_NtupleMaker.py
```

默认读取 `../../../BPH-RECOMINIAOD-<channel>_13TeV.root`，输出 `BPH-NTUPLE-<channel>_13TeV.root`；`<channel>` 为选择的 `SPS` 或 `DPS`。默认单线程、读取全部事件。

指定输入、输出和事件数：

```bash
cmsRun BPH_NtupleMaker.py era=2018 channel=SPS \
  inputFiles=file:input.root \
  outputFile=Ntuple_2018_SPS.root \
  maxEvents=-1
```

输入应包含 `slimmedMuons::RECO`、`packedPFCandidates::RECO` 和 `TriggerResults::HLT`。需要修改产品标签时，编辑 `NtupleMaker/python/NtupleMaker_cfi.py`。

## 4. CRAB 使用

CRAB 提交脚本由各项目的管理器或人工维护。使用共用入口时，在提交配置中指定：

```python
config.JobType.psetName = 'BPH_NtupleMaker.py'
config.JobType.pyCfgParams = ['era=2018', 'channel=DPS']
```

将 `era` 和 `channel` 改为本次生产所需值；未传入时采用 `year_config.py` 的默认值。提交前配置输入数据集、任务名称、输出标签和存储位置，并在脚本所在目录提交。
