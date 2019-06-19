import sys
import os
import time
import tkinter as tk
from tkinter import Frame
from tkinter import font
from _tkinter import TclError
from adb import adb


class Door(object):

    def __init__(self):
        self.onclick = False
        self.root = tk.Tk()
        self.ft = font.Font(name="Courier New", size=10, weight=font.BOLD)
        # self.msgbox = tk.Label(self)
        # self.msgbox.pack(side="top")
        # self.timer = tk.Label(self, font=self.ft)
        # self.timer.pack()
        # self.frm = Frame(self.root)
        # self.frm.pack(side="bottom")

    def shooting(self, **kwargs):
        st = tk.Button(self.root, height=10, width=10, font=self.ft, **kwargs)
        st.pack()
        self.onclick = True if not self.onclick else False

    # def stopShooting(self, **kwargs):
    #     st = self.button(self.root, height=2, width=3, font=self.ft, **kwargs)
    #     st.pack()
    #     self.flag = 'stop'

    def pop(self):
        self.root.mainloop()
