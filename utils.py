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
        else:
            self.process = Popen(self.command, stdout=PIPE)
            other.process = Popen(other.command, stdin=self.process.stdout, stdout=PIPE)
            self.process.stdout.close()
            other.stdout, other.stderr = other.process.communicate()
        return other

    def __is_standalone_command(self, command):
        patterns = [
            r"grep ?(-\w+| )+ *?\w+ *$",
            r"rev *$",
            r"cut +((-\w +'?[\w \d]'?|) *)* *$",
        ]
        matches = {re.match(pattern, command) for pattern in patterns}
        return matches == {None}

    def __call__(self, args=None):
        if len(self.command) == 1 and args:
            self.command = self.command + split(args)
        if self.__is_standalone_command("".join(self.command)):
            self.process = Popen(self.command, stdout=PIPE)
            self.stdout, self.stderr = self.process.communicate()
        return self

    def __str__(self):
        return self.stdout.decode("UTF-8")
