import threading
# import multiprocessing
from app.adb import adb
from app.door import Door
from app.serv import serv
from config import FFPLAY, ADB
from tkinter import messagebox

dr = Door()


def size(udid):
    srcsize = adb.screenSize(udid=udid)
    k = 350.0/float(srcsize[0])
    return srcsize if k >= 1 else ('350', str(int(float(srcsize[1])*k)))


def onclick(event):
    dr.x, dr.y = event.x, event.y
    # print(dr.x, dr.y)
    if dr.listRange:
        dr.select()
    if dr.iconRange['start']['xr'][0] <= dr.x <= dr.iconRange['start']['xr'][1] and \
            dr.iconRange['start']['yr'][0] <= dr.y <= dr.iconRange['start']['yr'][1]:
        dr.cleanMsg()
        dr.detect()
        dr.devices = {'sadlfoewfho': 232353523, 'UYOFHIOHIOFOH': 'oe8fhe98', 'sdfiyepvnwiue': 238720 - 238}
        if dr.devices:
            dr.cleanMsg()
            dr.options()
        if dr.selected:
            for ud in dr.udid:
                threading.Thread(target=adb.screening, kwargs=dict(size=size(str(ud)), udid=str(ud), noborder=False)).start()

    elif dr.iconRange['stop']['xr'][0] <= dr.x <= dr.iconRange['stop']['xr'][1] and \
            dr.iconRange['stop']['yr'][0] <= dr.y <= dr.iconRange['stop']['yr'][1]:
        if serv().alive(FFPLAY):
            if messagebox.askquestion(title="Ars", message=dr.onclickMsg['stop']).lower() == 'yes':
                serv(FFPLAY).stop()
        else:
            dr.cleanMsg()
            dr.processing(message=dr.onclickMsg['notScreening'])

    elif dr.iconRange['kill']['xr'][0] <= dr.x <= dr.iconRange['kill']['xr'][1] and \
            dr.iconRange['kill']['yr'][0] <= dr.y <= dr.iconRange['kill']['yr'][1]:
        serv(FFPLAY, ADB).stop()
        dr.cleanMsg()
        dr.processing(message=dr.onclickMsg['kill'])
    elif dr.iconRange['close']['xr'][0] <= dr.x <= dr.iconRange['close']['xr'][1] and \
            dr.iconRange['close']['yr'][0] <= dr.y <= dr.iconRange['close']['yr'][1]:
        if messagebox.askquestion(title="Ars", message=dr.onclickMsg['close']).lower() == 'yes':
            dr.close()


if __name__ == "__main__":
    # multiprocessing.freeze_support()
    dr.init_canvas()
    dr.canvas.bind("<Button-1>", onclick)
    dr.loop()

