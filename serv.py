import os


def alive(program):
    return True if os.popen("tasklist | findstr \"{0}\"".format(program)).readline() else False


def stop(program):
    os.popen("taskkill /f /im {0}".format(program))