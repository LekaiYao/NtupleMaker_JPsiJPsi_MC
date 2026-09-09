from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'MC2018_NTUPLE_DPS_v1_set1'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'BPH_NtupleMaker.py'
config.JobType.numCores = 1
config.JobType.maxMemoryMB = 2000
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '/UNSET/UNSET/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False
config.Data.outputDatasetTag = 'MC2018_NTUPLE_DPS_v1_set1'

config.Site.storageSite = 'T3_CH_CERNBOX'
config.Data.outLFNDirBase = '/store/user/leyao/26JJ/Ntuple/UL2018/DPS/'
