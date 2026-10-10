"""Expand the versioned premix snapshot into a self-contained CMSSW Process."""
from __future__ import print_function
import gzip
import hashlib
import json
import os

def read_snapshot(era):
    key = {'2016preVFP': 'UL16', '2016postVFP': 'UL16', '2017': 'UL17', '2018': 'UL18'}[era]
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'premix')
    with open(os.path.join(directory, key + '.json')) as handle:
        metadata = json.load(handle)
    with gzip.open(os.path.join(directory, key + '.txt.gz'), 'rb') as handle:
        content = handle.read()
    if hashlib.sha256(content).hexdigest() != metadata['sha256']:
        raise RuntimeError('Premix snapshot checksum mismatch: ' + key)
    files = content.decode('ascii').splitlines()
    dataset = metadata['dataset'].split('/')
    prefix = '/store/mc/RunIISummer20ULPrePremix/' + dataset[1] + '/PREMIX/' + dataset[2].split('-', 1)[1] + '/'
    if len(files) != metadata['file_count'] or len(files) != len(set(files)):
        raise RuntimeError('Premix snapshot count/uniqueness mismatch')
    if not all(f.startswith(prefix) and f.endswith('.root') for f in files):
        raise RuntimeError('Premix snapshot contains another dataset')
    return [str(f) for f in files]

def customise(process, era):
    import FWCore.ParameterSet.Config as cms
    process.mixData.input.fileNames = cms.untracked.vstring(read_snapshot(era))
    return process

if __name__ == '__main__':
    import sys
    # The cmsDriver filelist is generated from the same checksum-verified snapshot.
    print('\n'.join(read_snapshot(sys.argv[1])))
