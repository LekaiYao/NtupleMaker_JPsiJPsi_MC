# NtupleMaker 真值配对待办与 SPS/DPS 共用行为

记录日期：2026-09-09。用户要求本轮仅记录，不更新真值配对算法，也不开展本地事件测试。

## 当前实现

`setGENVariables` 遍历 `prunedGenParticles`，选择 PDG ID 为 443、status 为 2 且沿子代链找到两个末态 muon 的候选；按遍历顺序选择第一对，填写 `GEJpsi1_*`、`GEJpsi2_*`、`GEmu_*`。没有显式进行相反电荷检查、连续 J/ψ 副本去重或硬散射系统归属检查。

原有 `if(temp_JpsiMom[i] != temp_JpsiMom[j]) continue; // only for SPS` 仍被注释。母粒子访问已加空指针保护；这项保护不改变配对规则。当前没有 SPS/DPS 模式参数，也不从输入或输出文件名判断产生机制。

## 后续检查要求（尚未实施）

- 识别两个不同的物理 J/ψ，合并同一粒子的连续生成记录副本。
- 确认每个 J/ψ 的 μ⁺μ⁻ 衰变链，允许辐射光子，两个候选不共享真值 muon。
- 对当前 DPS fragment，追溯到同一次 pp 碰撞中的指定第一硬散射与 SecondHard，分别记录来源；不能仅凭母粒子不同、同 PV、status 或 hard-process 标记认定属于两个散射。
- 区分直接产生、χc/ψ(2S) feed-down、b-hadron 来源及额外散射来源，明确所研究信号的纳入范围。
- 对 SPS 检查两者是否归属同一硬散射；直接母粒子相同并非一般性的 SPS 定义。
- 先检查完整生成记录，再确认 HepMC/GenParticle 转换及 MiniAOD pruning 后是否仍保留判定所需信息；必要时在生成阶段保存来源关联。
- 来源不完整时记录“无法判定”，不以候选遍历顺序代替来源验证。

Pythia 文档说明 SecondHard 产生两次指定硬散射，第一/第二不保证按横动量排序，且两者均使用硬过程的状态码范围。参考：[Second Hard Process](https://pythia.org/latest-manual/SecondHardProcess.html)。具体索引、状态及来源映射须用本项目实际 Pythia 版本核验，不能直接套用固定事件行号。

## 当前 SPS/DPS 共用行为

两个输入均使用同一套 MC 真值选择、生成—重建 muon 匹配、muon/J/ψ 选择、顶点拟合、触发路径及 samePV 判据；没有按产生机制切换算法。samePV 来自四个匹配 packed candidate 的顶点索引是否相同，不是 SPS/DPS 分类器。analyze 最终填写事件树，候选函数提前返回并不等同于整事件被过滤。

当前输入为已归档的 31 事件 SPS 合并 MiniAOD，输出名仍为 `Ntuple_2016_DPS.root`。输出名仅是沿用参考配置的文件名，不代表输入被变成 DPS。本轮不修改该名称。产品标签已使用 `slimmedMuons::RECO`、`packedPFCandidates::RECO`，HLT 保持 `TriggerResults::HLT`；两种通道的当前合并生产配置采用同一产品接口。

SPS 和 DPS 的实际分布、重建效率、触发接受率及当前真值规则的可靠性可能不同，必须以后通过两种样本验证。当前迁入版本尚未编译或执行 NtupleMaker 事件测试。

## 后续状态补记：SPS 本地测试

2026-09-09 用户随后要求启用原有同母粒子条件并测试。现该条件已取消注释，31 事件 SPS 测试通过，31 个事件满足当前真值配对规则。上述“仍被注释”和“尚未编译或测试”描述保留为此前记录；当前状态以本补记及 README 为准。硬散射归属、去重和来源分类等待办仍未实施。

## 通道参数化补记

随后已将同母粒子条件改为 requireSameMother 配置参数，由 rootupleSPS/rootupleDPS 预设设置 true/false，C++ 共用且无需手动注释。当前运行入口选择 SPS。两个预设在同一 SPS 输入上的软件验证通过，SPS 输出全部分支与先前结果一致；未实施上述硬散射归属待办。

## 建仓库时的当前状态（2026-09-09）

当前入口已切换为 rootupleDPS，输入与输出均采用 DPS 名称。前文保留历次记录；通道参数化和 SPS 样本验证已完成，硬散射来源等物理待办仍未实施。
