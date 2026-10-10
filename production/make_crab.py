#!/usr/bin/env python3
"""Generate a user-specific CRAB configuration; never submit a task."""
import argparse
import re
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--era', required=True, choices=['2016preVFP','2016postVFP','2017','2018'])
    p.add_argument('--step', required=True, choices=['GENSIMDIGI','HLT','RECOMINIAOD','NTUPLE'])
    p.add_argument('--set', dest='batch', default='v3_set1')
    p.add_argument('--user', required=True, help='CMS username owning /store/user/USER')
    p.add_argument('--site', required=True, help='CRAB storageSite writable by this user')
    p.add_argument('--input', dest='dataset', help='Published output dataset of the preceding step')
    p.add_argument('--events', type=int, default=1000000000)
    p.add_argument('--events-per-job', type=int, default=100000)
    a = p.parse_args()
    if not re.fullmatch(r'v3_set[1-9][0-9]*', a.batch):p.error('--set must be v3_setN')
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', a.user):p.error('Invalid CMS username')
    if not re.fullmatch(r'T[0-3]_[A-Za-z0-9_]+', a.site):p.error('Invalid storage site')
    if a.events <= 0 or a.events_per_job <= 0:p.error('Event counts must be positive')
    if a.step != 'GENSIMDIGI':
        if not a.dataset or not re.fullmatch(r'/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/USER',a.dataset) or 'UNSET' in a.dataset:
            p.error('--input must be a real published /primary/processed/USER dataset')
    elif a.dataset:p.error('GENSIMDIGI has no --input')
    ntuple = a.step == 'NTUPLE'
    pset = 'NtupleMaker/NtupleMaker/test/BPH_NtupleMaker.py' if ntuple else 'BPH_'+a.step+'_DPS_13TeV_cfg.py'
    if not Path(pset).is_file():p.error('Run from the correct CMSSW/src after generating '+pset)
    request = 'MC'+a.era+'_'+a.step+'_DPS_'+a.batch
    if (Path('crab_projects')/('crab_'+request)).exists():p.error('A local task with this name already exists')
    lines = ['from CRABClient.UserUtilities import config', 'config = config()', '']
    def put(key,value):lines.append('config.'+key+' = '+repr(value))
    put('General.requestName',request)
    put('General.workArea','crab_projects')
    put('General.transferOutputs',True)
    put('General.transferLogs',True)
    put('JobType.pluginName','PrivateMC' if a.step=='GENSIMDIGI' else 'Analysis')
    put('JobType.psetName',pset)
    put('JobType.numCores',1 if ntuple else 2)
    put('JobType.maxMemoryMB',2000 if ntuple else 4000)
    put('JobType.allowUndistributedCMSSW',True)
    if ntuple:put('JobType.pyCfgParams',['era='+a.era,'channel=DPS'])
    if a.step=='GENSIMDIGI':
        suffix={'2016preVFP':'16preVFP','2016postVFP':'16postVFP','2017':'17','2018':'18'}[a.era]
        put('Data.outputPrimaryDataset','Pythia8_DPS_JpsiJpsi_UL'+suffix)
        put('Data.splitting','EventBased')
        put('Data.unitsPerJob',a.events_per_job)
        put('Data.totalUnits',a.events)
    else:
        put('Data.inputDataset',a.dataset)
        put('Data.inputDBS','phys03')
        put('Data.splitting','FileBased')
        put('Data.unitsPerJob',1)
    put('Data.publication',not ntuple)
    put('Data.outputDatasetTag',request)
    put('Data.outLFNDirBase','/store/user/'+a.user+'/JJMC/UL'+a.era+'/DPS/'+a.step)
    put('Site.storageSite',a.site)
    output=Path('crab_'+a.step+'_DPS_'+a.batch+'.py')
    with output.open('x') as handle:handle.write('\n'.join(lines)+'\n')
    print(str(output))

if __name__=='__main__':main()
