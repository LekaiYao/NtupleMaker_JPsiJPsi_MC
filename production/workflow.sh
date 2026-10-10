# Source after era.sh; MC_WORK is the directory containing both CMSSW releases.
in_release() {
  ( export SCRAM_ARCH="$2"
    cd "$MC_WORK/$1/src" || exit
    eval "$(scram runtime -sh)"
    source /cvmfs/cms.cern.ch/crab3/crab.sh prod
    "$3" "${@:4}" )
}

make_config() {
  local release="$MAIN_RELEASE" arch="$MAIN_ARCH"
  if [ "$1" = HLT ]; then release="$HLT_RELEASE"; arch="$HLT_ARCH"; fi
  local step="$1"; shift
  in_release "$release" "$arch" env -u PYTHONPATH -u PYTHONHOME python3 "$RECIPE/make_crab.py" \
    --era "$MC_ERA" --set "$MC_SET" --user "$CRAB_USER" --site "$CRAB_SITE" --step "$step" "$@"
}

crab_step() {
  local release="$MAIN_RELEASE" arch="$MAIN_ARCH"
  if [ "$1" = HLT ]; then release="$HLT_RELEASE"; arch="$HLT_ARCH"; fi
  local step="$1" action="$2"
  case "$action" in
    submit) in_release "$release" "$arch" crab submit -c "crab_${step}_DPS_${MC_SET}.py" ;;
    status) in_release "$release" "$arch" crab status -d "crab_projects/crab_MC${MC_ERA}_${step}_DPS_${MC_SET}" ;;
    getoutput) in_release "$release" "$arch" crab getoutput --xrootd -d "crab_projects/crab_MC${MC_ERA}_${step}_DPS_${MC_SET}" ;;
    *) echo 'Usage: crab_step STEP submit|status|getoutput' >&2; return 1 ;;
  esac
}
