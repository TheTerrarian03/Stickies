from tkinter import *
import classes as cs
from functions import getOS

# initial window setup with title
root = Tk()

# icon photo setting
if getOS() == "linux" or getOS() == "windows":
    # for linux and windows
    stickiesIcon = PhotoImage(file="ICON-flat.png")
    root.iconphoto(False, stickiesIcon)
elif getOS() == "macOS":
    # for macOS
    stickiesIcon = PhotoImage(file="ICON-smooth.png")
    root.iconphoto(False, stickiesIcon)

# make the class
mainWin = cs.MainWindow(root, version=2.6)

# run the mainloop, so the program actually, y'know, runs.
root.mainloop()
