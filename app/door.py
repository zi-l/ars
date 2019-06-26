import tkinter as tk
from tkinter import font, LEFT
from tkinter import messagebox
import threading

from app.serv import serv
from config import ADB, FFPLAY, PATH
from app.adb import adb


class Door(object):
    x, y = 0, 0
    icon_sq = {
        1: "start",
        2: "stop",
        3: "kill",
        "start": 1,
        "stop": 2,
        "kill": 3,
    }
    onclickMsg = {
        "start": "Start screening",
        "stop": "Stop screening?",
        "kill": "All processes killed",
        "close": "Quit?",

    }
    sizeWidth = 120
    sizeHeight = 40
    solidSize = 40
    textUnit = 25
    iconSize = 32
    miniSize = 10
    iconRevise = 5
    iconRange = {}
    listRange = {}

    def __init__(self, master=None, func: dict = None):
        self.func = func
        self.devices = {}
        self.root = tk.Tk() if not master else master
        # self.root.resizable(0, 0)  # prevent from size changing
        self.root.geometry("{0}x{1}+{2}+100".format(
            self.sizeWidth, self.sizeHeight, self.root.winfo_screenwidth() - self.sizeWidth - 200))
        self.ft = font.Font(name="Courier New", size=10, weight=font.BOLD)
        self.canvas = tk.Canvas(self.root)
        self.udid = []
        self.selected = False

    def create_canvas(self):
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.7)  # 窗口透明度30 %
        self.sizeHeight = self.solidSize + len(self.devices)*self.textUnit + 5 if len(self.devices) <= 1 else \
            self.solidSize + len(self.devices)*self.textUnit
        # print('self.sizeHeight:', self.sizeHeight)
        self.canvas.configure(width=self.sizeWidth)
        self.canvas.configure(height=self.sizeHeight)
        self.canvas.configure(bg="black")
        self.canvas.configure(highlightthickness=0)
        self.attachImage(self.canvas)
        self.root.iconbitmap(PATH("static/handshake.ico"))  # placed here instead of __init__()
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.move)
        self.canvas.bind("<Button-1>", self.onclick)

    def attachImage(self, canvas):
        icon_amount = len(self.icon_sq.keys())/2
        # distance between each icon
        xd = (self.sizeWidth - self.iconSize * icon_amount) / (icon_amount + 1)
        # yd = (self.sizeHeight - self.iconSize) / 2  # distance to the top
        yd = 4  # distance to the top
        # print(PATH("static/close.png"))
        self.imageClose = tk.PhotoImage(file=PATH("static/close.png"))
        canvas.create_image(self.sizeWidth, 0, anchor='ne', image=self.imageClose)
        self.iconRange['close'] = {"xr": (self.sizeWidth - self.miniSize + 1, self.sizeWidth),
                                   "yr": (0, self.miniSize - 1)}

        self.image1 = tk.PhotoImage(file=PATH("static/{0}.png".format(self.icon_sq[1])))
        canvas.create_image(self.sizeWidth - self.iconSize/2 - xd*self.icon_sq[self.icon_sq[1]],
                            yd+self.iconSize/2, anchor='center', image=self.image1)
        self.iconRange[self.icon_sq[1]] = {
            "xr": (self.sizeWidth - xd - self.iconSize + self.iconRevise, self.sizeWidth - xd),
            "yr": (yd + self.iconRevise / 2 if (yd + self.iconRevise / 2) >= self.miniSize else self.miniSize,
                   yd + self.iconSize - self.iconRevise / 2)}
        # print(str(self.icon_sq[1]) + ": ", self.iconRange[self.icon_sq[1]])

        self.image2 = tk.PhotoImage(file=PATH("static/{0}.png".format(self.icon_sq[2])))
        canvas.create_image(self.sizeWidth - 3*self.iconSize/2 - xd*self.icon_sq[self.icon_sq[2]],
                            yd+self.iconSize/2, anchor='center', image=self.image2)
        self.iconRange[self.icon_sq[2]] = {"xr": (self.sizeWidth-2*(xd+self.iconSize)+self.iconRevise,
                                                  self.sizeWidth-(2*xd+self.iconSize)-self.iconRevise),
                                           "yr": (yd + self.iconRevise / 2,
                                                  yd + self.iconSize - self.iconRevise / 2)}

        self.image3 = tk.PhotoImage(file=PATH("static/{0}.png".format(self.icon_sq[3])))
        canvas.create_image(self.sizeWidth - 5*self.iconSize/2 - xd*self.icon_sq[self.icon_sq[3]],
                            yd+self.iconSize/2, anchor='center',
                            image=self.image3)
        self.iconRange[self.icon_sq[3]] = {"xr": (self.sizeWidth-3*(xd+self.iconSize)+self.iconRevise,
                                                  self.sizeWidth-(3*xd+2*self.iconSize)-self.iconRevise),
                                           "yr": (yd + self.iconRevise / 2,
                                                  yd + self.iconSize - self.iconRevise / 2)}

        # self.image5 = tk.PhotoImage(file=PATH("static/mini.png"))
        # canvas.create_image(2, 0, anchor='nw', image=self.image5)
        # self.iconRange['mini'] = {"xr": (1, 11), "yr": (0, 4)}

    def options(self):
        self.sizeHeight = self.solidSize + len(self.devices) * self.textUnit + 5 if len(self.devices) <= 1 else \
            self.solidSize + len(self.devices) * self.textUnit
        self.root.geometry('{0}x{1}'.format(self.sizeWidth, self.sizeHeight))
        self.create_canvas()
        self.canvas.create_line(8, self.solidSize + 2, self.sizeWidth - 8, self.solidSize + 2, fill='green')
        space = (self.textUnit*len(self.devices) - 15)/float((len(self.devices)*3 - 1)/3)
        for ix, devName in enumerate(self.devices.keys()):
            txt_limit = 13 if str(devName).isupper() else 15
            tagId = self.canvas.create_text(
                (10, self.solidSize + 15 + space * ix),
                text=str(devName) if len(str(devName)) <= txt_limit+1 else str(devName)[:txt_limit] + "...", anchor='w',
                fill='orange', justify=LEFT)
            self.listRange[devName] = [(self.solidSize + 10 + space * ix,
                                                     self.solidSize + 10 + space * ix + 10), tagId]
        self.root.update()
        self.canvas.update()

    def move(self, event):
        self.root.overrideredirect(True)
        new_x = (event.x - self.x) + self.root.winfo_x()
        new_y = (event.y - self.y) + self.root.winfo_y()
        self.root.geometry("{0}x{1}+".format(self.sizeWidth, self.sizeHeight) + str(new_x) + "+" + str(new_y))

    def onclick(self, event):
        self.x, self.y = event.x, event.y
        # print(self.x, self.y)
        if self.listRange:
            for k, v in self.listRange.items():
                if v[0][0] <= self.y <= v[0][1]:
                    self.selected = True if not self.selected else False
                    txt_limit = 13 if str(k).isupper() else 15
                    self.canvas.itemconfigure(
                        v[1], text=str(k) if len(str(k)) <= txt_limit + 1 else str(k)[:txt_limit] + "...",
                        anchor='w', fill='green' if self.selected else 'orange', justify=LEFT)
                    self.canvas.update()
                    self.root.update()
                    if self.selected:
                        if self.devices[k] not in self.udid:
                            self.udid.append(self.devices[k])
                    else:
                        if self.devices[k] in self.udid:
                            self.udid.remove(self.devices[k])
                    break
        if self.iconRange['start']['xr'][0] <= self.x <= self.iconRange['start']['xr'][1] and \
                self.iconRange['start']['yr'][0] <= self.y <= self.iconRange['start']['yr'][1]:
            if not self.devices:
                messagebox.showinfo(title='Ars', message='Searching')
                self.devices = adb.nameUdid()
                self.options()
            if self.selected:
                # threading.Thread(target=self.func['start'], args=self.udid).start()
                for ud in self.udid:
                    self.func["start"](ud)

        elif self.iconRange['stop']['xr'][0] <= self.x <= self.iconRange['stop']['xr'][1] and \
                self.iconRange['stop']['yr'][0] <= self.y <= self.iconRange['stop']['yr'][1]:
            if serv().alive(FFPLAY):
                if messagebox.askquestion(title="Ars", message=self.onclickMsg['stop']).lower() == 'yes':
                    serv(FFPLAY).stop()
            else:
                messagebox.showinfo(title="Ars", message="No Screening ")
        elif self.iconRange['kill']['xr'][0] <= self.x <= self.iconRange['kill']['xr'][1] and \
                self.iconRange['kill']['yr'][0] <= self.y <= self.iconRange['kill']['yr'][1]:
            serv(FFPLAY, ADB).stop()
            messagebox.showinfo(title="Ars", message=self.onclickMsg['kill'])
        elif self.iconRange['close']['xr'][0] <= self.x <= self.iconRange['close']['xr'][1] and \
                self.iconRange['close']['yr'][0] <= self.y <= self.iconRange['close']['yr'][1]:
            if messagebox.askquestion(title="Ars", message=self.onclickMsg['close']).lower() == 'yes':
                self.close()
        # elif self.iconRange['mini']['xr'][0] <= self.x <= self.iconRange['mini']['xr'][1] and \
        #         self.iconRange['mini']['yr'][0] <= self.y <= self.iconRange['mini']['yr'][1]:
        #     self.root.overrideredirect(False)
        #     self.root.iconify()
        #     self.root.overrideredirect(True)

    def close(self):
        serv(ADB, FFPLAY).stop()
        self.root.destroy()

    def loop(self):
        self.root.mainloop()


