from tkinter import *
import tkinter.messagebox
import classes as cs
import functions as fcs

# initial window setup with title
root = Tk()

# icon photo setting
if fcs.getOS() == "linux" or fcs.getOS() == "windows":
    stickiesIcon = PhotoImage(file="ICON-linux-windows.png")
    root.iconphoto(False, stickiesIcon)
elif fcs.getOS() == "macOS":
    stickiesIcon = PhotoImage(file="ICON-macOS.png")
    root.iconphoto(False, stickiesIcon)

# make the class
mainWin = cs.MainWindow(root, version=2.4)

# run the mainloop, so the program actually, y'know, runs.
root.mainloop()
