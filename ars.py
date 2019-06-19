import os
import threading

from adb import adb, FFPLAY
from serv import serv
from door import Door
import tkinter as tk

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


def dpsize():
    srcsize = adb.screenSize()
    k = 350.0/float(srcsize[0])
    return srcsize if k >= 1 else ('350', str(int(float(srcsize[1])*k)))


def shoot():
    udid = adb.devices()[0] if adb.devices() else None
    adb.screening(size=dpsize(), udid=udid)


def run():
    t1 = threading.Thread(target=shoot)
    t1.start()


if __name__ == "__main__":
    door = Door()
    door.root.wm_attributes('-topmost', 1)
    door.root.geometry("12x35")
    door.remote(
        text=">",
        # image=tk.PhotoImage(PATH("favicon.png")) if door.onclick is False else tk.PhotoImage(PATH("favicon.png")),
        command=run)
    door.disconnect(
        text="ll",
        # image=tk.PhotoImage(PATH("favicon.png")) if door.onclick is False else tk.PhotoImage(PATH("favicon.png")),
        command=serv(FFPLAY).stop)
    door.loop()
