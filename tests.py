import sys
import os
import tkinter

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

print(sys.platform)

root = tkinter.Tk()
root.overrideredirect(True)
# root.attributes("-alpha", 0.3)窗口透明度70 %
root.attributes("-alpha", 0.7)  # 窗口透明度60 %
sizex = 100
sizey = 40
iconsize = 32
closesize = 16
root.geometry("{0}x{1}+{2}+100".format(sizex, sizey, root.winfo_screenwidth()-sizex-200))
canvas = tkinter.Canvas(root)
canvas.configure(width=sizex)
canvas.configure(height=sizey)
canvas.configure(bg="black")
canvas.configure(highlightthickness=0)
image1 = tkinter.PhotoImage(file=PATH("static/start.png"))
canvas.create_image(sizex - iconsize/2-(sizex-iconsize*3)/3, sizey/2, anchor='center', image=image1)
xr1 = (71, 94)
yr1 = (9, 31)
image2 = tkinter.PhotoImage(file=PATH("static/stop.png"))
canvas.create_image(sizex - iconsize/2-(sizex-iconsize*3)/3 - iconsize, sizey/2, anchor='center', image=image2)
xr2 = (38, 63)
yr2 = (6, 31)
image3 = tkinter.PhotoImage(file=PATH("static/kill.png"))
canvas.create_image(sizex - iconsize/2-(sizex-iconsize*3)/3 - iconsize*2, sizey/2, anchor='center', image=image3)
xr3 = (7, 30)
yr3 = (6, 31)
image4 = tkinter.PhotoImage(file=PATH("static/close.png"))
canvas.create_image(sizex, 0, anchor='ne', image=image4)
xr4 = (91, 100)
yr4 = (0, 8)
image5 = tkinter.PhotoImage(file=PATH("static/mini.png"))
canvas.create_image(2, 0, anchor='nw', image=image5)
xr5 = (0, 11)
yr5 = (0, 4)
canvas.pack()
x, y = 0, 0


def move(event):
    global x, y
    new_x = (event.x - x) + root.winfo_x()
    new_y = (event.y - y) + root.winfo_y()
    s = "100x40+" + str(new_x) + "+" + str(new_y)
    root.geometry(s)
    print("s = ", s)
    print(root.winfo_x(), root.winfo_y())
    print(event.x, event.y)
    print()


def button_1(event):
    global x, y
    x, y = event.x, event.y
    print("event.x, event.y = ", event.x, event.y)


canvas.bind("<B1-Motion>", move)
canvas.bind("<Button-1>", button_1)
root.mainloop()
