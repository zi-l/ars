import tkinter as tk
from tkinter import font
from tkinter import messagebox

from app.serv import serv
from config import ADB, FFPLAY, PATH


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
    sizeWidth = 100
    sizeHeight = 40
    iconSize = 32
    miniSize = 10
    iconRevise = 5
    iconRange = dict()

    def __init__(self, master=None, ui='canvas', func: dict = None):
        self.func = func
        self.root = tk.Tk() if not master else master
        self.root.resizable(0, 0)  # prevent from size changing
        self.root.geometry("{0}x{1}+{2}+100".format(
            self.sizeWidth, self.sizeHeight, self.root.winfo_screenwidth() - self.sizeWidth - 200))
        self.canvas = tk.Canvas(self.root)
        self.ft = font.Font(name="Courier New", size=10, weight=font.BOLD)
        self.ui = ui
        if self.ui == 'canvas':
            self.create_canvas()

    def remote(self, **kwargs):
        st = tk.Button(self.root, height=2, width=2, font=self.ft, **kwargs)
        st.pack(side="left")

    def disconnect(self, **kwargs):
        st = tk.Button(self.root, height=2, width=2, font=self.ft, **kwargs)
        st.pack(side="left")

    def killall(self, **kwargs):
        st = tk.Button(self.root, height=2, width=2, font=self.ft, **kwargs)
        st.pack(side="left")

    def create_canvas(self):
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.7)  # 窗口透明度30 %
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
        yd = (self.sizeHeight - self.iconSize) / 2  # distance to the top

        self.imageClose = tk.PhotoImage(file=PATH("static/close.png"))
        canvas.create_image(self.sizeWidth, 0, anchor='ne', image=self.imageClose)
        self.iconRange['close'] = {"xr": (self.sizeWidth - self.miniSize + 1, self.sizeWidth),
                                   "yr": (0, self.miniSize - 1)}

        self.image1 = tk.PhotoImage(file=PATH("static/{0}.png".format(self.icon_sq[1])))
        canvas.create_image(self.sizeWidth - self.iconSize/2 - xd*self.icon_sq[self.icon_sq[1]],
                            self.sizeHeight / 2, anchor='center', image=self.image1)
        self.iconRange[self.icon_sq[1]] = {
            "xr": (self.sizeWidth - xd - self.iconSize + self.iconRevise, self.sizeWidth - xd),
            "yr": (yd + self.iconRevise / 2 if (yd + self.iconRevise / 2) >= self.miniSize else self.miniSize,
                   yd + self.iconSize - self.iconRevise / 2)}
        # print(str(self.icon_sq[1]) + ": ", self.iconRange[self.icon_sq[1]])

        self.image2 = tk.PhotoImage(file=PATH("static/{0}.png".format(self.icon_sq[2])))
        canvas.create_image(self.sizeWidth - 3*self.iconSize/2 - xd*self.icon_sq[self.icon_sq[2]],
                            self.sizeHeight / 2, anchor='center', image=self.image2)
        self.iconRange[self.icon_sq[2]] = {"xr": (self.sizeWidth-2*(xd+self.iconSize)+self.iconRevise,
                                                  self.sizeWidth-(2*xd+self.iconSize)-self.iconRevise),
                                           "yr": (yd + self.iconRevise / 2,
                                                  yd + self.iconSize - self.iconRevise / 2)}

        self.image3 = tk.PhotoImage(file=PATH("static/{0}.png".format(self.icon_sq[3])))
        canvas.create_image(self.sizeWidth - 5*self.iconSize/2 - xd*self.icon_sq[self.icon_sq[3]],
                            self.sizeHeight / 2, anchor='center',
                            image=self.image3)
        self.iconRange[self.icon_sq[3]] = {"xr": (self.sizeWidth-3*(xd+self.iconSize)+self.iconRevise,
                                                  self.sizeWidth-(3*xd+2*self.iconSize)-self.iconRevise),
                                           "yr": (yd + self.iconRevise / 2,
                                                  yd + self.iconSize - self.iconRevise / 2)}

        # self.image5 = tk.PhotoImage(file=PATH("static/mini.png"))
        # canvas.create_image(2, 0, anchor='nw', image=self.image5)
        # self.iconRange['mini'] = {"xr": (1, 11), "yr": (0, 4)}

    def move(self, event):
        self.root.overrideredirect(True)
        new_x = (event.x - self.x) + self.root.winfo_x()
        new_y = (event.y - self.y) + self.root.winfo_y()
        self.root.geometry("{0}x{1}+".format(self.sizeWidth, self.sizeHeight) + str(new_x) + "+" + str(new_y))

    def onclick(self, event):
        self.x, self.y = event.x, event.y
        # print("event.x, event.y = ", event.x, event.y)
        if self.iconRange['start']['xr'][0] <= self.x <= self.iconRange['start']['xr'][1] and \
                self.iconRange['start']['yr'][0] <= self.y <= self.iconRange['start']['yr'][1]:
            messagebox.showinfo(title="Ars", message="Start screening", parent=self.canvas)
            self.func["start"]()
        elif self.iconRange['stop']['xr'][0] <= self.x <= self.iconRange['stop']['xr'][1] and \
                self.iconRange['stop']['yr'][0] <= self.y <= self.iconRange['stop']['yr'][1]:
            if serv().alive(FFPLAY):
                if messagebox.askquestion(title="Ars", message="Stop screening?").lower() == 'yes':
                    serv(FFPLAY).stop()
            else:
                messagebox.showinfo(title="Ars", message="No Screening running")
        elif self.iconRange['kill']['xr'][0] <= self.x <= self.iconRange['kill']['xr'][1] and \
                self.iconRange['kill']['yr'][0] <= self.y <= self.iconRange['kill']['yr'][1]:
            serv(FFPLAY, ADB).stop()
            messagebox.showinfo(title="Ars", message="All processes killed")
        elif self.iconRange['close']['xr'][0] <= self.x <= self.iconRange['close']['xr'][1] and \
                self.iconRange['close']['yr'][0] <= self.y <= self.iconRange['close']['yr'][1]:
            if messagebox.askquestion(title="Ars", message="Quit?").lower() == 'yes':
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


# if __name__ == "__main__":
#     # multiprocessing.freeze_support()
#     door = Door(func=dict(start=run))
#     door.loop()


