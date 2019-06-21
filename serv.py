import os
from config import msgbx


class serv(object):

    def __init__(self, *programs):
        self.program = programs

    @msgbx
    def alive(self, prog=None):
        return True if os.popen(
            "tasklist | findstr \"{0}\"".format(self.program if not prog else prog)).readline() else False

    @msgbx
    def stop(self, *prog):
        if prog:
            self.program = prog
        for p in self.program:
            os.popen("taskkill /f /im {0}".format(p))
