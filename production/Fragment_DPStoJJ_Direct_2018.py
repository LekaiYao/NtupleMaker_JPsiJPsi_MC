import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

FourMuonFilter = cms.EDFilter("FourLepFilter", # require 4-mu in the final state
        MinPt = cms.untracked.double(3.3),
        MaxPt = cms.untracked.double(4000.0),
        MaxEta = cms.untracked.double(2.5),
        MinEta = cms.untracked.double(0.),
        ParticleID = cms.untracked.int32(13)
)

JpsiJpsiFilter = cms.EDFilter("MCParticlePairFilter",  # define a J/psi pair; currently not scheduled
        MinPt = cms.untracked.vdouble(1.0,1.0),
        MaxPt = cms.untracked.vdouble(4000.0,4000.0),
        MaxEta = cms.untracked.vdouble( 2.5,2.5),
        MinEta = cms.untracked.vdouble(-2.5,-2.5),
        ParticleID1 = cms.untracked.vint32(443, -443),
        ParticleID2 = cms.untracked.vint32(443, -443),
        MinInvMass = cms.untracked.double(1.0),
        MaxInvMass = cms.untracked.double(16.0),
)

generator = cms.EDFilter("Pythia8GeneratorFilter",
    crossSection = cms.untracked.double(1.0),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'Charmonium:gg2ccbar(3S1)[3S1(1)]g = on,off',
            'Charmonium:gg2ccbar(3S1)[3S1(1)]gm = on, off',
            'Charmonium:gg2ccbar(3S1)[3S1(8)]g = on, off',
            'Charmonium:qqbar2ccbar(3S1)[3S1(8)]g = on,off',
            'Charmonium:qg2ccbar(3S1)[3S1(8)]q = on,off',
            'Charmonium:qqbar2ccbar(3S1)[3S1(8)]g = on,off',
            'Charmonium:gg2ccbar(3S1)[1S0(8)]g = on,off',
            'Charmonium:qg2ccbar(3S1)[1S0(8)]q = on,off',
            'Charmonium:qqbar2ccbar(3S1)[1S0(8)]g = on,off',
            'Charmonium:gg2ccbar(3S1)[3PJ(8)]g = on,off',
            'Charmonium:qg2ccbar(3S1)[3PJ(8)]q = on,off',
            'Charmonium:qqbar2ccbar(3S1)[3PJ(8)]g = on,off',
#           'Charmonium:all = on',
            'SecondHard:generate = on',
            'SecondHard:Charmonium = on',
#           'PhaseSpace:mHatMin = 10.',
#           'PhaseSpace:pTHatMin = 1.',
#           'PhaseSpace:pTHatMinSecond = 1.',
#           'PhaseSpace:pTHatMinDiverge = 0.1',
            '10441:onMode = off',
            '10441:onIfMatch = 443',
            '20443:onMode = off',
            '20443:onIfMatch = 443',
            '443:onMode = off',
            '443:onIfMatch = -13 13',
            '100443:onMode = off',
            '100443:onIfMatch = 443',
            'PartonLevel:MPI = on',              #! no multiparton interactions
            'PartonLevel:ISR = on',              #! no initial-state radiation
            'PartonLevel:FSR = on',              #! no final-state radiation
            'HadronLevel:all = on',              #! continue after parton level
            'HadronLevel:Hadronize = on',        #! no hadronization
            'HadronLevel:Decay = on',            #! no decays
        ),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'processParameters'
        ),
    ),
    comEnergy = cms.double(13000.0),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(1)
)

ProductionFilterSequence = cms.Sequence(generator*FourMuonFilter)
