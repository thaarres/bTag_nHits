from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'btagHits'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'config.py'

config.Data.inputDataset = '/ZprimeBB/thaarres-ZprimeBB_GEN_SIM_DIGI_RECO-b3c215846157ef4e588d255b6fc9b9fe/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'btagHits_Ana_ZprimeBB'

config.Site.storageSite = 'T3_CH_PSI'