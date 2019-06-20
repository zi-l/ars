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
    # run()
    door = Door()
    door.root.wm_attributes('-topmost', 1)
    door.root.geometry("10x37+{0}+100".format(door.root.winfo_screenwidth()-300))
    door.root.title("ARS")
    door.root.attributes("-alpha", 0.8)
    # door.root.overrideredirect(True)  # 需要自定义位置
    door.killall(
        text="X", fg='green', bg='LightYellow',
        # image=tk.PhotoImage(file=PATH("static/tkcolor.png")),
        command=serv(FFPLAY, ADB).stop)
    door.disconnect(
        text="ll", bg='green',
        # image=tk.PhotoImage(file=PATH("static/stop.png")),
        command=serv(FFPLAY).stop)
    door.remote(
        text=">", bg='green',
        # image=tk.PhotoImage(file=PATH("static/start.png")),
        command=run)
    door.loop()
