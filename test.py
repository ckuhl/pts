#!/usr/bin/python3.5
import logging
import os
import subprocess
import sys

import yaml


# set up logging
log = logging.Logger(__name__)
log.setLevel(logging.INFO)

# gather files
files = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) ]
testfile = None

# check that a testfile is there
if 'Testfile' in files:
    testfile = yaml.load_all(open('Testfile', 'r'))
else:
    sys.exit()

# test counts
num_tests = {'succeeded': 0, 'failed': 0, 'total': 0}

# loop through test cases
for suite in testfile:
    program = suite['program']
    log.warning('Testing: ' + str(program) + ' ' + '=' * (80 - 1 - len('Testing: ' + str(program))))
    for test in suite['tests']:
        try:
            output = subprocess.run([*program, test['args']], stdout=subprocess.PIPE, input=test['in'].encode('utf-8'))
        except KeyError:
            output = subprocess.run([*program], stdout=subprocess.PIPE, input=test['in'].encode('utf-8'))

        output = output.stdout.decode('utf-8').strip()

        if output != test['out']:
            log.error('Test failed: ' + test['name'])

            log.warning('  In: ' + test['in'])
            log.warning('  Expected: ' + test['out'])
            log.warning('  Out: ' + output)
            log.error('=' * 80)

            num_tests['failed'] += 1
        else:
            log.debug('Test succeeded: ' + test['name'])
            log.debug('=' * 80)
            num_tests['succeeded'] += 1
        num_tests['total'] += 1


log.warning(str(num_tests['total']) + ' tests run, with ' + str(num_tests['succeeded']) + ' successful and ' + str(num_tests['failed']) + ' failing')

