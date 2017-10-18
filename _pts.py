import logging
import subprocess


log = logging.getLogger(__name__)


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
            self.stderr = test['stderr']
            self.has_stderr = True
        except KeyError:
            self.has_stderr = False


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


    def run(self, test):
        """
        Run a given test

        :param test: Test
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
                stderr=subprocess.PIPE)

        stdout, stderr = '', ''

        if self.is_piped:
            for p in self.pipe_to:
                pipe_run = subprocess.run(p,
                        input=cmd_in.stdout,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

                stderr += cmd_in.stderr.decode('utf-8')
                cmd_in = pipe_run

        # gather outputs
        stdout += cmd_in.stdout.decode('utf-8')
        stderr += cmd_in.stderr.decode('utf-8')

        if test.has_stdout and stdout != test.stdout:
            is_successful = False
            log.warning('Expected stdout:\n%s', test.stdout)
            log.warning('Actual stdout:\n%s', stdout)
            if len(test.stdout) != len(stdout):
                log.warning('Expected len: %d,\tactual len: %d',
                        len(test.stdout), len(stdout))

        if test.has_stderr and stderr != test.stderr:
            is_successful = False
            log.warning('Expected stderr:\n%s', test.stderr)
            log.warning('Actual stderr:\n', stderr)
            if len(test.stderr) != len(stderr):
                log.warning('Expected len: %d,\tactual len: %d',
                        len(test.stderr), len(stderr))

        return is_successful

