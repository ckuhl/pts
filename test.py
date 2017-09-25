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


# get files in invoking directory
files = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) ]
testfile = None

# look for a Testfile
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
    log.info('Testing: %s %s',
            program,
            '=' * (80 - 1 - len('Testing: ' + str(program))))
    try:
        log.info(suite['name'])
    except KeyError:
        pass

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
            log.error('Test failed: %s', test['name'])
            log.warning('  stdin: %s', test['in'])

            if stdout != expected_stdout:
                log.warning('  expected_stdout: %s', expected_stdout)
                log.warning('  stdout: ' + stdout)
                if len(expected_stdout) != len(stdout):
                    log.warning('  expected len: %d,  Actual len: %d',
                            len(expected_stdout), len(stdout))

            if stderr != expected_stderr:
                log.warning('  expected_stderr: %s', expected_stderr)
                log.warning('  stderr: %s', stderr)
                if len(expected_stderr) != len(stderr):
                    log.warning('  expected len: %d, actual len: %d',
                            len(expected_stderr), len(stderr))

            num_tests['failed'] += 1

        else:
            log.debug('Test succeeded: %s', test['name'])
            num_tests['succeeded'] += 1

        num_tests['total'] += 1

    log.debug('=' * 80)

log.warning('%d tests run, with %d successful and %d failing',
        num_tests['total'], num_tests['succeeded'], num_tests['failed'])

