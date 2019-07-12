import os
from config import msgbx, OS


class serv(object):

    def __init__(self, *programs):
        self.program = programs

    @msgbx
    def alive(self, prog):
        cmd = "tasklist | findstr" if OS.startswith("win") else "ps ax|grep"
        result = os.popen("{0} {1}".format(cmd, prog)).readline()
        return True if result and not str(result.strip()).endswith(prog) else False

    @msgbx
    def stop(self, *prog):
        if prog:
            self.program = prog
        cmd = "taskkill /f /im" if OS.startswith("win") else "killall -2"
        for p in self.program:
            os.popen("{0} {1}".format(cmd, p))
