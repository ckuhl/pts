#!/usr/bin/python3.5
import argparse
import logging
import os
import subprocess
import sys

import yaml


# command line options
parser = argparse.ArgumentParser(
        prog='pts - Python Test Suite',
        description='Run plaintext tests against scripts')
parser.add_argument(
        '--verbose', '-v',
        help='add verbosity (-v to -vvvv)',
        action='count',
        default=0)
args = parser.parse_args()

# configure logging (logger and console handler)
verb_log = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG,
}
log = logging.getLogger(__name__)
log.setLevel(verb_log[args.verbose])
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)


# beginning of script
files = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) ]
testfile = None

# check that a testfile is there
if 'Testfile' in files:
    testfile = yaml.load_all(open('Testfile', 'r'))
else:
    log.info('No Testfile found in current directory')
    sys.exit()

# test counter
num_tests = {'succeeded': 0, 'failed': 0, 'total': 0}

# loop through test cases
for suite in testfile:
    program = suite['program']
    log.warning('Testing: ' + str(program) + ' ' + '=' * (80 - 1 - len('Testing: ' + str(program))))
    for test in suite['tests']:

        # Check for arguments
        try:
            command = [*program, *test['args']]
        except KeyError:
            command = [*program]

        run = subprocess.run(command,
                             input=test['in'].encode('utf-8'),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        # gather outputs
        stdout = run.stdout.decode('utf-8')
        stderr = run.stderr.decode('utf-8')
        expected_stdout = test['out']
        try:
            expected_stderr = test['stderr']
        except KeyError:
            expected_stderr = ''

        # error logging
        if stdout != expected_stdout or stderr != expected_stderr:
            log.error('Test failed: ' + test['name'])
            log.warning('  stdin: ' + test['in'])

            if stdout != expected_stdout:
                log.warning('  expected_stdout: ' + expected_stdout)
                log.warning('  stdout: ' + stdout)

            if stderr != expected_stderr:
                log.warning('  expected_stderr: ' + expected_stderr)
                log.warning('  stderr: ' + stderr)
                log.error('=' * 80)

            num_tests['failed'] += 1

        else:
            log.debug('Test succeeded: ' + test['name'])
            num_tests['succeeded'] += 1

        num_tests['total'] += 1

    log.debug('=' * 80)

log.info(str(num_tests['total']) + ' tests run, with ' + str(num_tests['succeeded']) + ' successful and ' + str(num_tests['failed']) + ' failing')

