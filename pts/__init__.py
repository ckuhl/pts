import argparse
import difflib
import logging
import os
import subprocess
import sys

import yaml


log = logging.getLogger(__name__)


def main():
    __version__ = (0, 0, 3)

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
            '--quiet', '-q',
            help='reduce verbosity (-q to -qqqq)',
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

    # combine q/v to allow aliases (e.g. alias pts='pts -vvvv' and then use -q)
    verbosity_level = max(0, min(5, args.verbose - args.quiet))

    logging.basicConfig(level=verb_log[verbosity_level], format='')
    log = logging.getLogger(__name__)

    ts = TestSuite(directory=args.directory)
    ts.run()



def visual_diff(expected, actual):
    return ''.join(difflib.ndiff(expected.splitlines(keepends=True),
        actual.splitlines(keepends=True)))


class Test(object):
    """
    A Test is a set of inputs, arguments, and expected outputs
    """
    def __init__(self, test):
        """
        Set up all the parts of the test, and set flags

        :param test: A dictionary of field names : field values
        :return: None
        """
        self.name = test['name']
        self.input = test['in']
        try:
            self.args = test['args']
            self.has_args = True
        except KeyError:
            self.has_args = False

        try:
            self.stdout = test['out']
            self.has_stdout = True
        except KeyError:
            self.has_stdout = False
        try:
            if self.has_stdout:
                raise KeyError
            self.stdout = test['stdout']
            self.has_stdout = True
        except KeyError:
            self.has_stdout = False

        try:
            self.stdout_contains = test['stdout_contains']
            self.has_stdout_membership = True
        except KeyError:
            self.has_stdout_membership = False

        try:
            self.stderr = test['stderr']
            self.has_stderr = True
        except KeyError:
            self.has_stderr = False

        try:
            self.stderr_contains = test['stderr_contains']
            self.has_stderr_membership = True
        except KeyError:
            self.has_stderr_membership = False


class Suite(object):
    """
    A Suite contains a given command, and the tests that should be run on it
    """
    def __init__(self, suite):
        """
        Construct the suite from a dictionary

        :param suite: Dict of field : parameter mappings
        :return: None
        """
        self.program = suite['program']
        try:
            self.pipe_to = suite['pipe_to']
            self.is_piped = True
        except KeyError:
            self.is_piped = False
        self.name = suite['name']
        try:
            self.tags = set(suite['tags'])
            self.has_tags = True
        except KeyError:
            self.has_tags = False
        self.tests = [Test(x) for x in suite['tests']]
        try:
            self.file_in = suite['file_in']
            self.has_file_in = True
        except KeyError:
            self.has_file_in = False


    def run(self, test, directory):
        """
        Run a given test

        :param test: Test
        :param directory: path to run tests from
        :return: Bool
        """

        log.info('%s %s', test.name, '-' * (80 - 1 - len(test.name)))
        is_successful = True

        command = self.program
        if test.has_args:
            command = [*command, *test.args]

        test_in = test.input
        if self.has_file_in:
            test_in = open(self.file_in, 'r').read() + test_in
        test_in = test_in.encode('utf-8')

        cmd_in = subprocess.run(command,
                input=test_in,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=directory)

        stdout, stderr = '', ''

        if self.is_piped:
            for p in self.pipe_to:
                pipe_run = subprocess.run(p,
                        input=cmd_in.stdout,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=directory)

                stderr += cmd_in.stderr.decode('utf-8')
                cmd_in = pipe_run

        # gather outputs
        stdout += cmd_in.stdout.decode('utf-8')
        stderr += cmd_in.stderr.decode('utf-8')

        if test.has_stdout and stdout != test.stdout:
            is_successful = False
            # log.warning('Expected stdout:\n%s', test.stdout)
            # log.warning('Actual stdout:\n%s', stdout)
            log.warning(visual_diff(test.stdout, stdout))
            if len(test.stdout) != len(stdout):
                log.warning('Expected len: %d,\tactual len: %d',
                        len(test.stdout), len(stdout))

        if test.has_stderr and stderr != test.stderr:
            is_successful = False
            log.warning('Expected stderr:\n%s', test.stderr)
            log.warning('Actual stderr:\n%s', stderr)
            if len(test.stderr) != len(stderr):
                log.warning('Expected len: %d,\tactual len: %d',
                        len(test.stderr), len(stderr))

        if test.has_stdout_membership and test.stdout_contains not in stdout:
            is_successful = False
            log.warning('Expected to find "%s" in stdout\n',
                    test.stdout_contains)
            log.info('Actual stdout:\n%s', stdout)

        if test.has_stderr_membership and test.stderr_contains not in stderr:
            is_successful = False
            log.warning('Expected to find "%s" in stderr\n',
                    test.stderr_contains)
            log.info('Actual stderr:\n%s', stderr)

        return is_successful


class TestSuite(object):
    """
    Wrapper class for Suites, which in turn wrap Tests
    """
    def __init__(self, directory=None, test_name=None):
        """
        Configure accoring to command line args

        :param directory: Directory to run in (defaults to current directory)
        :return: None
        """
        self.directory = os.curdir
        if directory:
            self.directory = os.path.join(self.directory, directory)

        self.test_name = test_name

    def run(self):
        """
        Run the appropriate tests according to command line input
        """
        files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
        # look for a Testfile
        if 'Testfile' in files:
            testfile = yaml.load_all(open(os.path.join(self.directory, 'Testfile'), 'r'))
        else:
            log.info('No Testfile found in current directory')
            sys.exit()

        # test counter
        num_tests = {'succeeded': 0, 'failed': 0, 'total': 0}

        # loop through suites
        for suite in [Suite(x) for x in testfile]:
            # check that suite name matches
            try:
                if suite.has_tags and self.test_name:
                    if self.test_name in suite.tags:
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
                if suite.run(test, self.directory):
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

