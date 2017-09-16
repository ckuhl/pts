#!/usr/bin/python3.5
import logging
import os
import subprocess
import sys

import yaml


# set up logging
log = logging.Logger(__name__)

# gather files
files = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) ]
testfile = None

# check that a testfile is there
if 'Testfile' in files:
    testfile = yaml.load(open('Testfile', 'r'))
else:
    sys.exit()

# loop through test cases
program = testfile['program']
for test in testfile['tests']:
    try:
        output = subprocess.run([*program, test['args']], stdout=subprocess.PIPE, input=test['in'].encode('utf-8'))
    except KeyError:
        output = subprocess.run([*program], stdout=subprocess.PIPE, input=test['in'].encode('utf-8'))

    output = output.stdout.decode('utf-8').strip()

    if output != test['out']:
        log.error('Test failed: ' + test['name'])

        log.warning('In:' + test['in'])
        log.warning('Expected:' + test['out'])
        log.warning('Out:' + output)
    else:
        log.debug('Test succeeded' + test['name'])

