
import FWCore.ParameterSet.Config as cms
rootuple = cms.EDAnalyzer(
    'NtupleMaker',
    era = cms.string('2016postVFP'),
    vertexFilter = cms.string('hltVertexmumuFilterJpsiMuon'),
    l3Filter = cms.string('hltTripleMuL3PreFiltered0'),
    l1Filter = cms.string('hltL1sTripleMu0'),
    channel = cms.string('SPS'),
    requireSameMother = cms.bool(True),
    # dimuons = cms.InputTag("onia2MuMuPAT"),
    # conversions = cms.InputTag("oniaPhotonCandidates","conversions"),# "conversions"
    # TriggerSummaryAOD = cms.InputTag("hltTriggerSummaryAOD", "", "HLT"),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),# MINAOD #, "", "PAT"
    # primaryVertices = cms.InputTag("offlinePrimaryVertices"),# Monte-Carlo
    offlineBeamSpot = cms.InputTag("offlineBeamSpot"),#, "", "RECO"
    muons = cms.InputTag("slimmedMuons", "", "RECO"),# MINIAOD
    # muons = cms.InputTag("oniaSelectedMuons"),# Monte-Carlo
    TriggerResults = cms.InputTag("TriggerResults", "", "HLT"),
    triggerList = cms.untracked.vstring(
        # 'HLT_Dimuon0_Jpsi3p5_Muon2_v',
        'HLT_Dimuon0_Jpsi_Muon_v',
        #'HLT_Trimuon5_3p5_2_Upsilon_Muon_v',       #2018  HLT string
        #'HLT_TrimuonOpen_5_3p5_2_Upsilon_Muon_v',  #2018 HLT string
        #'HLT_Trimuon2_Upsilon5_Muon_v'            #2017B HLT string
        #'HLT_Trimuon5_3p5_2_Upsilon_Muon_v'       #2017 C,D, E and F HLT string
        #'HLT_Dimuon0_Upsilon_Muon_v',             #2016 HLT string 
        #'HLT_Dimuon0_Phi_Barrel_v',               #2016 HLT string 
        #'HLT_Dimuon13_Upsilon_v',                 #2016 HLT string 
        #'HLT_Dimuon8_Upsilon_Barrel_v',           #2016 HLT string
    ),
    Candidates = cms.InputTag("packedPFCandidates", "", "RECO"),
    SecondSource = cms.SecSource(
        "EmbeddedRootSource",
        fileNames = cms.untracked.vstring(
            'SpyFileNameWhichNeedsToBeSet SiStripSpyEventMatcher.SpySource.fileNames'
        ),
        sequential = cms.untracked.bool(True),
    )
)

# Channel presets share all reconstruction and input settings.
rootupleSPS = rootuple.clone(channel = 'SPS', requireSameMother = True)
rootupleDPS = rootuple.clone(channel = 'DPS', requireSameMother = False)

# Year and production channel are independent; original presets retain 2016 settings.
rootuple2018 = rootuple.clone(
    era = '2018',
    triggerList = cms.untracked.vstring('HLT_Dimuon0_Jpsi3p5_Muon2_v'),
    vertexFilter = 'hltVertexmumuFilterJpsiMuon3p5',
    l3Filter = 'hltTripleMuL3PreFiltered222',
    l1Filter = 'hltL1TripleMu5SQ3SQ0OQDoubleMu53SQOSMassMax9',
)
rootuple2018SPS = rootuple2018.clone(channel = 'SPS', requireSameMother = True)
rootuple2018DPS = rootuple2018.clone(channel = 'DPS', requireSameMother = False)
