# 2018 触发匹配核验

依据本地官方 CMSSW_10_2_16_UL 的 HLTrigger/Configuration/python/HLT_2018v32_cff.py，路径为 HLT_Dimuon0_Jpsi3p5_Muon2_v5。

| 匹配用途 | filter | 插件类型 |
| --- | --- | --- |
| L1 | hltL1TripleMu5SQ3SQ0OQDoubleMu53SQOSMassMax9 | HLTL1TSeed |
| L3 | hltTripleMuL3PreFiltered222 | HLTMuonL3PreFilter |
| 顶点 | hltVertexmumuFilterJpsiMuon3p5 | HLTDisplacedmumuFilter |

三个模块均在目标路径上。参考 chensh 2018 源码把 Vtx 与 L1 字符串对调；本项目将按插件类型和模块用途修正。需要进一步用本地输出检查 trigger object 标签及匹配结果，不能以编译成功替代这项验证。

年份与 SPS/DPS 通道作为独立配置维度。保留现有母粒子空指针保护、同母粒子参数及真值配对待办，不改变硬散射来源规则。

## 本地事件核验结果

2026-09-09：SPS 请求 1000 个生成事件，28 个通过原过滤；GENSIMDIGI、HLT、RECOMINIAOD 均退出 0，事件标识一致。MiniAOD 目标路径通过 17 个事件。

muon 内嵌触发对象中的标签出现次数：顶点 68，L3 102，L1 112。SPS/DPS 预设各输出 28 个 Ntuple 事件、28 个有效真值对事件、6 个重建对候选；其中 4 个事件通过触发匹配、4 个事件满足 samePV。两次测试输入均是 SPS，不构成 DPS 物理验证。

诊断时发现 PyROOT 直接调用 TriggerObjectStandAlone(obj) 可选中基类构造并清空标签；最终核验使用 C++ 显式复制构造和 unpackNamesAndLabels，与生产 C++ 行为一致。没有为此修改生产匹配算法。

HLT/RECO 日志有非致命 TkDetLayers、TrajectoryNotPosDef 诊断；退出码、FrameworkJobReport、输出事件标识和产品均核验通过，不将它们描述为零日志告警。
