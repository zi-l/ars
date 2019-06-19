import os
import time

from adb import adb, ADB, FFPLAY
from serv import stop, alive
from door import Door
import tkinter as tk

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


def dpsize():
    srcsize = adb.screenSize()
    k = 480.0/float(srcsize[0])
    return srcsize if k >= 1 else ('480', str(int(float(srcsize[1])*k)))


def run():
    udid = adb.devices()[0] if adb.devices() else None
    adb.screening(size=dpsize(), udid=udid)


def kill():
    stop(FFPLAY)
    stop(ADB)


if __name__ == "__main__":
    # run()
    door = Door()
    door.root.wm_attributes('-topmost', 1)
    door.root.geometry("40x60")
    print(door.onclick)
    door.shooting(
        # image=tk.PhotoImage(PATH("favicon.png")) if door.onclick is False else tk.PhotoImage(PATH("favicon.png")),
        command=run if door.onclick is False else kill)
    door.pop()
    # time.sleep(3)
    # stop(FFPLAY)
    # stop(ADB)
    # print(alive(FFPLAY))
