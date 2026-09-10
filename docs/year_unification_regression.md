# 年份整合回归核验

日期：2026-09-10。修改在 ULPythia2016postVFP 的 CMSSW_10_6_20/src/NtupleMaker、main 分支完成。

整合前 main 已备份至 v2_ULPythia2016postVFP，提交 fd3a787；2018 基准来自 v2_ULPythia2018，提交 4f05e55。CRAB 文件与修改前 SHA256 一致，用户原有未提交修改未纳入本次提交。

## 方法

使用两个年份原有 SPS MiniAOD 作为固定输入，在 cmssw-el7、cmsenv 后用统一代码分别运行 SPS/DPS 预设。没有重新生成上游 MC，从而可以直接比较相同事件。

2016 基准为 config_archive/tests/ntuple_channels/Ntuple_{SPS,DPS}_on_SPS.root；2018 基准为原 SPS Ntuple 及 DPS_on_SPS Ntuple。新产物、运行命令、日志、FrameworkJobReport 和完整比较报告位于 2016 项目的 config_archive/tests/year_unification_20260910/。

按 run、lumi、event 对齐，验证输入与输出事件标识一致、所有树分支名称和类型一致，再比较全部标量和向量元素。对应 NaN 视为相同；其他非有限数变化不通过。数值容差为 |a-b| <= 1e-10 * max(1, |a|, |b|)。同时记录精确不相等的元素及差异明细，不以容差通过掩盖差异。

## 最终结果

| 年份 | 预设 | 事件数 | 分支数 | 比较元素数 | 非精确相等元素数 | 最大绝对差异 |
| --- | --- | --- | --- | --- | --- | --- |
| 2016postVFP | SPS | 31 | 84 | 6614 | 3 | 6.94e-18 |
| 2016postVFP | DPS | 31 | 84 | 6614 | 3 | 6.94e-18 |
| 2018 | SPS | 28 | 84 | 7081 | 0 | 0 |
| 2018 | DPS | 28 | 84 | 7081 | 0 | 0 |

四个 cmsRun 均退出 0，FrameworkJobReport 无 FrameworkError；没有超出容差的物理分支变化。微小差异位于浮点末位，与数值舍入量级一致；具体分支和值见 comparison.json。树结构、事件集合、有效真值配对及触发匹配计数保持一致。

ROOT 中新增 era 元数据，configuration 元数据增加年份和 filter 参数，这些是预期的配置记录变化，不属于物理树分支变化。

四组合的配置加载、GlobalTag、默认输入输出名称、单线程设置及 CRAB protocol 0 序列化检查通过；不支持的年份和通道明确报错，clone 之间的配置修改互不影响。最终入口显式注册输出参数，避免 VarParsing 内置分析模式自动加后缀改变默认文件名。

## 结论与范围

在现有 2016 和 2018 SPS 小样本上，年份整合保持原 Ntuple 物理结果，可将共用物理操作集中在 main 维护。DPS 预设也进行了软件回归，但其输入仍为 SPS；本次不证明真实 DPS 样本的物理适配性，也没有更新硬散射来源等真值配对待办。
