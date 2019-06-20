import tkinter as tk
from tkinter import font
from serv import serv
from adb import ADB, FFPLAY


class Door(object):

    def __init__(self):
        self.onclick = False
        self.root = tk.Tk()
        self.ft = font.Font(name="Courier New", size=10, weight=font.BOLD)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        # self.msgbox = tk.Label(self)
        # self.msgbox.pack(side="top")
        # self.timer = tk.Label(self, font=self.ft)
        # self.timer.pack()
        # self.frm = Frame(self.root)
        # self.frm.pack(side="bottom")

    def remote(self, **kwargs):
        st = tk.Button(self.root, height=2, width=2, font=self.ft, **kwargs)
        st.pack(side="left")
        # self.onclick = True if not self.onclick else False

    def disconnect(self, **kwargs):
        st = tk.Button(self.root, height=2, width=2, font=self.ft, **kwargs)
        st.pack(side="left")

    def killall(self, **kwargs):
        st = tk.Button(self.root, height=2, width=2, font=self.ft, **kwargs)
        st.pack(side="left")

    def close(self):
        serv(ADB, FFPLAY).stop()
        self.root.destroy()

    def loop(self):
        self.root.mainloop()