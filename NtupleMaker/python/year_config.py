# -*- coding: utf-8 -*-
# 年份和通道选择；CRAB 配置由项目单独维护。
DEFAULT_ERA = '2016postVFP'
DEFAULT_CHANNEL = 'DPS'

YEAR_SETTINGS = {
    '2016postVFP': {
        'globalTag': '106X_mcRun2_asymptotic_v13',
        'triggerPath': 'HLT_Dimuon0_Jpsi_Muon_v',
        'vertexFilter': 'hltVertexmumuFilterJpsiMuon',
        'l3Filter': 'hltTripleMuL3PreFiltered0',
        'l1Filter': 'hltL1sTripleMu0',
    },
    '2018': {
        'globalTag': '106X_upgrade2018_realistic_v15_L1v1',
        'triggerPath': 'HLT_Dimuon0_Jpsi3p5_Muon2_v',
        'vertexFilter': 'hltVertexmumuFilterJpsiMuon3p5',
        'l3Filter': 'hltTripleMuL3PreFiltered222',
        'l1Filter': 'hltL1TripleMu5SQ3SQ0OQDoubleMu53SQOSMassMax9',
    },
}

# preVFP shares the postVFP trigger definition; only conditions differ.
YEAR_SETTINGS['2016preVFP'] = dict(
    YEAR_SETTINGS['2016postVFP'],
    globalTag='106X_mcRun2_asymptotic_preVFP_v9',
)

# 2017 shares the 2018 trigger definition; conditions follow UL17.
YEAR_SETTINGS['2017'] = dict(
    YEAR_SETTINGS['2018'],
    globalTag='106X_mc2017_realistic_v8',
)

def getYearSettings(era):
    if era not in YEAR_SETTINGS:
        raise ValueError('Unsupported MC era: %s; choose %s' % (era, ', '.join(sorted(YEAR_SETTINGS))))
    return dict(YEAR_SETTINGS[era])
