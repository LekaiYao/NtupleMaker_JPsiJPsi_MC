import FWCore.ParameterSet.Config as cms
from NtupleMaker.NtupleMaker.year_config import getYearSettings

# Shared reconstruction and input products for merged RECO+MiniAOD.
_base = cms.EDAnalyzer(
    'NtupleMaker',
    primaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
    offlineBeamSpot = cms.InputTag('offlineBeamSpot'),
    muons = cms.InputTag('slimmedMuons', '', 'RECO'),
    TriggerResults = cms.InputTag('TriggerResults', '', 'HLT'),
    Candidates = cms.InputTag('packedPFCandidates', '', 'RECO'),
    SecondSource = cms.SecSource(
        'EmbeddedRootSource',
        fileNames = cms.untracked.vstring('SpyFileNameWhichNeedsToBeSet SiStripSpyEventMatcher.SpySource.fileNames'),
        sequential = cms.untracked.bool(True),
    ),
)

def makeNtuple(era, channel):
    settings = getYearSettings(era)
    if channel not in ('SPS', 'DPS'):
        raise ValueError('Unsupported MC channel: %s' % channel)
    return _base.clone(
        era = cms.string(era),
        channel = cms.string(channel),
        requireSameMother = cms.bool(channel == 'SPS'),
        triggerList = cms.untracked.vstring(settings['triggerPath']),
        vertexFilter = cms.string(settings['vertexFilter']),
        l3Filter = cms.string(settings['l3Filter']),
        l1Filter = cms.string(settings['l1Filter']),
    )

# Keep existing import names for both previously validated configurations.
rootuple = makeNtuple('2016postVFP', 'SPS')
rootupleSPS = rootuple.clone()
rootupleDPS = makeNtuple('2016postVFP', 'DPS')
rootuple2018 = makeNtuple('2018', 'SPS')
rootuple2018SPS = rootuple2018.clone()
rootuple2018DPS = makeNtuple('2018', 'DPS')
