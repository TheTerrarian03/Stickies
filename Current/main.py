from tkinter import *
import tkinter.messagebox
import classes as cs

# initial window setup with title
root = Tk()

# icon photo setting
stickiesIcon = PhotoImage(file="ICON.png")
root.iconphoto(False, stickiesIcon)

# make the class
mainWin = cs.MainWindow(root, version=2.4)

# run the mainloop, so the program actually, y'know, runs.
root.mainloop()

print("Banana")
