# Source this file with one argument: 2016preVFP, 2016postVFP, 2017 or 2018.
MC_ERA=${1:?source production/era.sh YEAR}
MAIN_RELEASE=CMSSW_10_6_20
MAIN_ARCH=slc7_amd64_gcc700
HLT_KEEP_ARGS=()
case "$MC_ERA" in
  2016preVFP|2016postVFP)
    MC_GT=106X_mcRun2_asymptotic_v13
    MC_CMSSW_ERA=Run2_2016
    if [ "$MC_ERA" = 2016preVFP ]; then
      MC_GT=106X_mcRun2_asymptotic_preVFP_v9
      MC_CMSSW_ERA=Run2_2016_HIPM
    fi
    BEAMSPOT=Realistic25ns13TeV2016Collision
    HLT_RELEASE=CMSSW_8_0_33_UL
    HLT_ARCH=slc7_amd64_gcc530
    HLT_GT=80X_mcRun2_asymptotic_2016_TrancheIV_v6
    HLT_MENU=25ns15e33_v4
    HLT_ERA=Run2_2016
    HLT_KEEP_ARGS=(--outputCommand 'keep *_mix_*_*,keep *_genPUProtons_*_*' --inputCommands 'keep *,drop *_*_BMTF_*,drop *PixelFEDChannel*_*_*_*')
    PREMIX_KEY=UL16
    ;;
  2017)
    MC_GT=106X_mc2017_realistic_v8
    MC_CMSSW_ERA=Run2_2017
    BEAMSPOT=Realistic25ns13TeVEarly2017Collision
    HLT_RELEASE=CMSSW_9_4_14_UL_patch1
    HLT_ARCH=slc7_amd64_gcc630
    HLT_GT=94X_mc2017_realistic_v15
    HLT_MENU=2e34v40
    HLT_ERA=Run2_2017
    PREMIX_KEY=UL17
    ;;
  2018)
    MC_GT=106X_upgrade2018_realistic_v15_L1v1
    MC_CMSSW_ERA=Run2_2018
    BEAMSPOT=Realistic25ns13TeVEarly2018Collision
    HLT_RELEASE=CMSSW_10_2_16_UL
    HLT_ARCH=slc7_amd64_gcc700
    HLT_GT=102X_upgrade2018_realistic_v15
    HLT_MENU=2018v32
    HLT_ERA=Run2_2018
    PREMIX_KEY=UL18
    ;;
  *) echo "Unsupported era: $MC_ERA" >&2; return 1 ;;
esac
export MC_ERA MAIN_RELEASE MAIN_ARCH MC_GT MC_CMSSW_ERA BEAMSPOT
export HLT_RELEASE HLT_ARCH HLT_GT HLT_MENU HLT_ERA PREMIX_KEY
