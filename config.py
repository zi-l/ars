import os
from tkinter import messagebox
from functools import wraps

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
FFPLAY = "ffplay.exe"
ADB = "adb.exe"


def msgbx(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            messagebox.showerror(title="ARS: Error", message=e)
            raise InterruptedError
    return wrapper


def adb_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "Android Debug Bridge" not in os.popen("adb").readline():
            messagebox.showerror(title="ARS: Error", message="adb not found")
            raise InterruptedError
        return func(*args, **kwargs)
    return wrapper