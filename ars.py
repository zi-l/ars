from adb import adb
import os
import time


def dpsize():
    srcsize = adb.screenSize()
    k = 480.0/float(srcsize[0])
    return srcsize if k >= 1 else ('480', str(int(float(srcsize[1])*k)))


def stop(program="ffplay.exe"):
    os.popen("taskkill /f /im {0}".format(program))


def run():
    udid = adb.devices()[0] if adb.devices() else None
    adb.screening(size=dpsize(), udid=udid)


if __name__ == "__main__":
    run()
    # time.sleep(3)
    # stop()
    # stop("adb.exe")
