# 2016preVFP 本地验证

2026-09-10，在独立 ULPythia2016preVFP 中完成 cmssw-el7、cmsenv、编译与本地四步测试。共用 C++、cfi 工厂和运行入口与 main 0e16c87 逐字一致；仅新增年份预设和本地默认选择。preVFP 复用 postVFP 的触发设置，GlobalTag 为 106X_mcRun2_asymptotic_preVFP_v9。

## 配置与结果

三年份（2016preVFP、2016postVFP、2018）与 SPS/DPS 六组合预设检查通过。SPS requireSameMother=True，DPS=False；生产默认 2016preVFP/DPS，输入产品为 RECO。CRAB protocol 0 序列化检查通过。

GENSIMDIGI 使用 CMSSW_10_6_20、Run2_2016_HIPM；HLT 使用 CMSSW_8_0_33_UL、Run2_2016；RECOMINIAOD 使用 CMSSW_10_6_20、Run2_2016_HIPM。1000 个 SPS 生成事件中 28 个通过原过滤，三步均退出 0、输出 28 事件，逐事件 run/lumi/event 一致。MiniAOD 的 muon、packed 候选和生成粒子产品以及 HLT 信息均有效。

同一份 SPS MiniAOD 分别用 SPS 和 DPS 配置读取：均退出 0，输出各 28 事件，28 个有效真值对事件、5 个重建对候选、4 个触发匹配事件、3 个 samePV 事件。验证元数据中的年份、通道及同母粒子开关。此项证明两种配置的软件兼容，不替代真实 DPS 物理验证。

## 沿用的 L1 辅助分支问题

目标路径 HLT_Dimuon0_Jpsi_Muon_v5 在 14/28 事件接受。MiniAOD 匹配对象中 hltVertexmumuFilterJpsiMuon 出现 62 次，hltTripleMuL3PreFiltered0 出现 93 次。原 postVFP 配置的 hltL1sTripleMu0 出现 0 次；CMSSW_8_0_33_UL 的 HLT_25ns15e33_v4_cff.py 实际目标路径使用 hltL1sTripleMu0orTripleMu500。

当前 C++ 的事件匹配条件只组合 Vtx 和 L3，故不受该 L1 标签影响；L1 查询另用于 REevt_L1muPtMax，该辅助量在本样本的候选中为 0。不能据此判定真实 L1 muon 横动量为 0。按 pre/post 触发配置一致的约定，此次保留原设置，未改变共用物理实现。后续若启用此辅助量，须一并讨论并验证两期配置修正。

完整运行日志、FrameworkJobReport、事件检查及触发对象报告位于 ULPythia2016preVFP/config_archive/tests/SPS 和 config_archive/logs。年份预设证据为 tests/year_presets.json，共用代码校验值为 tests/shared_code_audit.json。
