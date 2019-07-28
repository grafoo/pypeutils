from subprocess import Popen, PIPE
from shlex import split
import sys
import re


class Util(object):
    def __init__(self, command):
        self.command = split(command)
        self.stdout = None

    def __or__(self, other):
        if self.stdout:
            other.process = Popen(other.command, stdin=PIPE, stdout=PIPE)
            other.stdout, other.stderr = other.process.communicate(input=self.stdout)
            other.command = other.command[0:1]
        else:
            self.process = Popen(self.command, stdout=PIPE)
            other.process = Popen(other.command, stdin=self.process.stdout, stdout=PIPE)
            self.process.stdout.close()
            other.stdout, other.stderr = other.process.communicate()
            self.command = self.command[0:1]
            other.command = other.command[0:1]
        return other

    def __is_standalone_command(self, command):
        # TODO: Check if e.g. docopt (http://docopt.org/) can be used to
        # determine when command requires reading from stdin via pipe, instead
        # of matching all command as regex patterns.
        patterns = [
            r"grep( +-\w+| +-\w)* +?\w+ *$",
            r"rev *$",
            r"cut( +-\w ?['\"]?[\x00-\x7f]['\"]?| +-\w)+ *$",
        ]
        matches = {re.match(pattern, command) for pattern in patterns}
        return matches == {None}

    def __call__(self, args=None):
        if len(self.command) == 1 and args:
            self.command = self.command + split(args)
        if self.__is_standalone_command(" ".join(self.command)):
            self.process = Popen(self.command, stdout=PIPE)
            self.stdout, self.stderr = self.process.communicate()
            self.command = self.command[0:1]
        return self

    def __str__(self):
        return self.stdout.decode("UTF-8")

    def __invert__(self):
        sys.stdout.write(str(self))
