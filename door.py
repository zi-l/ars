import tkinter as tk
from tkinter import Frame
from tkinter import font
from _tkinter import TclError


class PopUp(tk.Frame):

    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.flag = None
        self.pack()
        self.root = master
        self.msgbox = tk.Label(self)
        self.msgbox.pack(side="top")
        self.ft = font.Font(name="Courier New", size=20, weight=font.BOLD)
        self.timer = tk.Label(self, font=self.ft)
        self.timer.pack()
        self.frm = Frame(self.root)
        self.frm.pack(side="bottom")

    # 生成文本计时器，每秒刷新一次弹窗
    def count_down(self, count_time: int):
        try:
            for sec in range(count_time, 0, -1):
                minutes = int(sec / 60)
                seconds = int(sec % 60)
                self.timer['text'] = '%s:%s' % (minutes, seconds)
                self.root.update()
                if sec % 15 == 0:
                    self.play_sound()
                time.sleep(1)
            self.flag = -1
            self.root.destroy()
        except TclError:
            pass

    def get_flag(self):
        return self.flag

    # 播放系统提示音
    def play_sound(self):
        if sys.platform == 'darwin':
            os.system("osascript -e 'beep'")
        elif sys.platform == 'win32' or sys.platform == 'cygwin':
            import winsound
            winsound.PlaySound('alert', winsound.SND_ASYNC)