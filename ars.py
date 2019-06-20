import os
import threading

from adb import adb, FFPLAY, ADB
from serv import serv
from door import Door
import tkinter as tk

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


def dpsize():
    srcsize = adb.screenSize()
    k = 350.0/float(srcsize[0])
    return srcsize if k >= 1 else ('350', str(int(float(srcsize[1])*k)))


def shoot():
    udid = adb.devices()[0]
    adb.screening(size=dpsize(), udid=udid, noborder=False)


def run():
    t1 = threading.Thread(target=shoot)
    t1.start()


if __name__ == "__main__":
    door = Door(func=run)
    door.create_canvas()
    door.loop()
    # run()

