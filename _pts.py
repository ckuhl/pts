import logging
import subprocess


log = logging.getLogger(__name__)


class Test(object):
    def __init__(self, test):
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
    def __init__(self, suite):
        self.program = suite['program']
        try:
            self.pipe_to = suite['pipe_to']
            self.is_piped = True
        except KeyError:
            self.is_piped = False
        self.name = suite['name']
        self.tags = suite['tags']
        self.tests = [Test(x) for x in suite['tests']]


    def run(self, test):
        success = True

        command = [*self.program]
        if test.has_args:
            command = [*command, *test.args]

        run = subprocess.run(command,
                input=test.input.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        stdout, stderr = '', ''

        if self.is_piped:
            for p in self.pipe_to:
                pipe_run = subprocess.run(p,
                        input=run.stdout,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

                stderr += run.stderr.decode('utf-8')
                run = pipe_run

        # gather outputs
        stdout += run.stdout.decode('utf-8')
        stderr += run.stderr.decode('utf-8')

        if test.has_stdout and stdout != test.stdout:
            success = False
            log.warning('expected_stdout: %s', test.stdout)
            log.warning('stdout: ' + stdout)
            if len(test.stdout) != len(stdout):
                log.warning('expected len: %d,  Actual len: %d',
                        len(test.stdout), len(stdout))

        if test.has_stderr and stderr != test.stderr:
            success = False
            log.warning('expected_stderr: %s', test.stderr)
            log.warning('stderr: ' + stderr)
            if len(test.stderr) != len(stderr):
                log.warning('expected len: %d,  Actual len: %d',
                        len(test.stderr), len(stderr))

        if success:
            return True
        else:
            return False

