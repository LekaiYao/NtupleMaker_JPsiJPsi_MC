#!/usr/bin/env python
from __future__ import print_function

import os
import sys


if len(sys.argv) != 2:
    raise SystemExit('Usage: compact_GENSIMDIGI_cfg.py BPH_GENSIMDIGI_*_13TeV_cfg.py')
path = os.path.abspath(sys.argv[1])
with open(path, 'rb') as stream:
    original = stream.read()
lines = original.splitlines(True)
marker = b'process.mixData.input.fileNames = cms.untracked.vstring('
matches = [index for index, line in enumerate(lines) if line.startswith(marker)]
if len(matches) != 1:
    raise RuntimeError('Expected exactly one premix fileNames assignment in %s; found %d' % (path, len(matches)))
index = matches[0]
if b'load_premix.py' not in b''.join(lines[index + 1:]):
    raise RuntimeError('External premix loader is missing after the assignment in %s' % path)
compact_line = marker + b')\n'
if lines[index] == compact_line:
    print('Already compact: %s' % path)
    raise SystemExit(0)
if len(lines[index]) < 10000 or b'/store/mc/' not in lines[index]:
    raise RuntimeError('Refusing to replace an unexpected premix assignment in %s' % path)
lines[index] = (b'# Premix LFNs are loaded from NtupleMaker/production/premix by load_premix.py below.\n' + compact_line)
updated = b''.join(lines)
temporary = path + '.compact.tmp'
if os.path.exists(temporary):
    raise RuntimeError('Temporary file already exists: %s' % temporary)
with open(temporary, 'wb') as stream:
    stream.write(updated)
os.chmod(temporary, os.stat(path).st_mode)
with open(path, 'rb') as stream:
    if stream.read() != original:
        os.unlink(temporary)
        raise RuntimeError('Source changed during compaction: %s' % path)
os.rename(temporary, path)
print('Compacted %s from %d to %d bytes' % (path, len(original), len(updated)))
