import os
import threading

from adb import adb
from door import Door

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


def size():
    srcsize = adb.screenSize()
    k = 350.0/float(srcsize[0])
    return srcsize if k >= 1 else ('350', str(int(float(srcsize[1])*k)))


def run():
    udid = adb.devices()[0]
    t1 = threading.Thread(target=adb.screening, kwargs=dict(size=size(), udid=udid, noborder=False))
    t1.start()


if __name__ == "__main__":
    door = Door(func=dict(start=run))
    door.create_canvas()
    door.loop()

