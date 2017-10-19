#!/usr/bin/python3.5
import argparse
import logging
import os
import sys

import yaml

import _pts


__version__ = (0, 0, 1)

# command line options
parser = argparse.ArgumentParser(
        prog='PythonTestSuite',
        description='Run plaintext tests against scripts')
parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {v[0]}.{v[1]}.{v[2]}'.format(v=__version__))
parser.add_argument(
        'test_name',
        help='optional test name to run only one suite',
        nargs='?',
        default='')
parser.add_argument(
        '--verbose', '-v',
        help='add verbosity (-v to -vvvv)',
        action='count',
        default=0)
parser.add_argument(
        '--directory', '-d',
        help='specify the directory containing the Testfile',
        action='store',
        default='')

args = parser.parse_args()

# configure logging (logger and console handler)
verb_log = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG,
}

# comment out format to get modules to work together
logging.basicConfig(level=verb_log[args.verbose], format='')
log = logging.getLogger(__name__)


# get files in invoking directory
directory = os.curdir
if args.directory:
    directory = os.path.join(directory, args.directory)
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
# look for a Testfile
if 'Testfile' in files:
    testfile = yaml.load_all(open(os.path.join(directory, 'Testfile'), 'r'))
else:
    log.info('No Testfile found in current directory')
    sys.exit()

# test counter
num_tests = {'succeeded': 0, 'failed': 0, 'total': 0}

# loop through suites
for suite in [_pts.Suite(x) for x in testfile]:
    # check that suite name matches
    try:
        if suite.has_tags and args.test_name:
            if args.test_name in suite.tags:
                log.info('Testing: %s %s',
                        suite.program,
                        '=' * (80 - 1 - len('Testing: ' + str(suite.program))))
            else:
                log.debug('Skipping: %s %s',
                        suite.program,
                        '=' * (80 - 1 - len('Skipping: ' + str(suite.program))))
                continue
        log.info("%s %s",
                suite.name,
                '=' * (80 - 1 - len(suite.name)))
    except KeyError:
        pass

    # run tests
    for test in suite.tests:
        if suite.run(test, directory):
            num_tests['succeeded'] += 1
        else:
            num_tests['failed'] += 1
        num_tests['total'] += 1

    log.info('=' * 80)


# Testing summary
if num_tests['failed']:
    log.warning('%d tests run: %d succeeded and %d failed',
            num_tests['total'], num_tests['succeeded'], num_tests['failed'])
else:
    log.warning('%d tests run: All succeeded', num_tests['total'])

