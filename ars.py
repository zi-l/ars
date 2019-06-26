import threading
# import multiprocessing
from app.adb import adb
from app.door import Door


def size(udid):
    srcsize = adb.screenSize(udid=udid)
    k = 350.0/float(srcsize[0])
    return srcsize if k >= 1 else ('350', str(int(float(srcsize[1])*k)))


def run(udid):
    t1 = threading.Thread(target=adb.screening, kwargs=dict(size=size(udid), udid=udid, noborder=False))
    t1.start()


if __name__ == "__main__":
    # multiprocessing.freeze_support()
    door = Door(func=dict(start=run))
    door.create_canvas()
    door.loop()

