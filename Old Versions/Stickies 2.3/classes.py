from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import functions as fcs
import os

class MainWindow:
    def __init__(self, master):
        ### set master obj
        self.master = master

        ### sticky objects and stuff
        self.stickies = fcs.getAllStickies()
        if fcs.getLastOpen():
            self.stickies = fcs.setNewActive(self.stickies, fcs.getLastOpen())
        else:
            self.stickies[0].active = True

        # text box for entering info
        self.textBox = Text(master)
        self.textBox.pack(expand=True, fill='both')

        ### menu bar
        # main top menu
        self.menu = Menu(master)
        master.config(menu=self.menu)
        # file sub-menu
        self.fileMenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="New Sticky", accelerator="CMD-N", command=self.newSticky)
        self.fileMenu.add_command(label="Open", accelerator="CMD-O", command=self.loadStickies)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Save Sticky", accelerator="CMD-S", command=self.saveActiveSticky)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.exitWindow)
        # edit sub-menu
        self.editMenu = Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.editMenu)
        self.editMenu.add_command(label="Undo", accelerator="CMD-Z", state=DISABLED)
        self.editMenu.add_command(label="Redo", accelerator="CMD-Shift-Z", state=DISABLED)
        self.editMenu.add_command(label="Sorry, there is no Undo or Redo...\n   >:D", state=DISABLED)
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Select all", accelerator="CMD-A", command=lambda: self.master.focus_get().event_generate("<Command-a>"))
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Cut", accelerator="CMD-X", command=lambda: self.master.focus_get().event_generate("<<Cut>>"))
        self.editMenu.add_command(label="Copy", accelerator="CMD-C", command=lambda: self.master.focus_get().event_generate("<<Copy>>"))
        self.editMenu.add_command(label="Paste", accelerator="CMD-V", command=lambda: self.master.focus_get().event_generate("<<Paste>>"))
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Clear Sticky", accelerator="CMD-Delete", command=self.clearSticky)
        self.editMenu.add_separator()
        self.editMenu.add_command(label="All To Lowercase", command=self.allToLowercase)
        self.editMenu.add_command(label="Line To Lowercase", command=self.lineToLowercase, state=DISABLED)
        self.editMenu.add_command(label="All To Uppercase", command=self.allToUppercase)
        self.editMenu.add_command(label="Line To Uppercase", command=self.lineToUppercase, state=DISABLED)
        self.editMenu.add_command(label="To Chaos. Don't do it. Please.", command=self.fillerFunction, state=DISABLED)
        # view sub-menu
        self.viewMenu = Menu(self.menu)
        self.menu.add_cascade(label="View", menu=self.viewMenu)
        self.viewMenu.add_command(label="Go Fullscreen", command=self.fillerFunction, state=DISABLED)
        self.viewMenu.add_separator()
        self.viewMenu.add_radiobutton(label="Show Line Number", command=self.fillerFunction, state=DISABLED)
        # help command in main menu
        self.helpMenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(label="Get Help", command=self.fillerFunction, state=DISABLED)
        self.helpMenu.add_command(label="About Stickies", command=self.fillerFunction, state=DISABLED)
        # bind all stuff for hotkeys and keybaord shortcuts
        self.master.bind_all("<Command-o>", self.loadStickies)
        self.master.bind_all("<Command-n>", self.newSticky)
        self.master.bind_all("<Command-Delete>", self.clearSticky)
        self.master.bind_all("<Command-s>", self.saveActiveSticky)

        ### call the reset function
        self.resetWidgets()
    
    ### Menu functions (in order of command added)
    def newSticky(self, event=None):
        print("Making new Sticky")
        newStickyTitle = fcs.makeNewSticky(returnTitle=True)
        print(newStickyTitle)
        self.saveActiveSticky()
        self.stickies = fcs.getAllStickies()
        self.stickies = fcs.setNewActive(self.stickies, newStickyTitle)
        self.resetWidgets()
        fcs.setLastOpen(fcs.rOA(self.stickies).title)

    def loadStickies(self, event=None):
        print("Loading Stickies...")
        filetypes = (("Sticky Saves", ".sticky"), ("All Files", "*.*"))
        chosenPath = tkinter.filedialog.askopenfilename(title='Open a file', initialdir=os.curdir+"/SAVES", filetypes=filetypes)
        if chosenPath:
            chosenStickyPath = chosenPath.split("/")[-2]+"/"+chosenPath.split("/")[-1]
            self.stickies = fcs.setNewActive(self.stickies, fcs.returnObjWithSamePath(self.stickies, chosenStickyPath).title)
            self.resetWidgets()
            fcs.setLastOpen(fcs.returnObjWithSamePath(self.stickies, chosenStickyPath).title)

    def saveActiveSticky(self, event=None):
        print("Saving Sticky with title: " + fcs.rOA(self.stickies).title)
        fcs.rOA(self.stickies).setText(self.textBox.get("1.0", "end"))
        fcs.rOA(self.stickies).save()
        print("Done Saving Sticky.")

    def exitWindow(self, event=None):
        title = "Exit Stickies v2.3"
        exitConfirm = tkinter.messagebox.askyesno(title, "Are you sure you want to quit?")
        if exitConfirm:
            quit()
    
    def clearSticky(self, event=None):
        fcs.rOA(self.stickies).content = "Silence."
        self.resetWidgets(setColors=False)
    
    def allToLowercase(self, event=None):
        self.saveActiveSticky()
        fcs.rOA(self.stickies).content = fcs.rOA(self.stickies).content.lower()
        self.resetWidgets(setColors=False)
    
    def lineToLowercase(self, event=None):
        self.saveActiveSticky()
    
    def allToUppercase(self, event=None):
        self.saveActiveSticky()
        fcs.rOA(self.stickies).content = fcs.rOA(self.stickies).content.upper()
        self.resetWidgets(setColors=False)
    
    def lineToUppercase(self, event=None):
        self.saveActiveSticky()

    ### Other functions
    def fillerFunction(self):
        print("Unfortunately, this button hasn't been assigned any functionality yet.")
        tkinter.messagebox.showerror("ERROR! No Functionality Has Been Added!", "Unfortunately, this button hasn't been assigned any functionality yet.")
    
    def resetWidgets(self, setText=True, setColors=True):
        if setText:
            # delete first
            self.textBox.delete("0.0", "end")
            # then insert needed text
            self.textBox.insert("0.0", fcs.rOA(self.stickies).content)
        if setColors:
            # print(fcs.rOA(self.stickies).colors)
            self.textBox.config(bg=("#"+fcs.rOA(self.stickies).colors["main"]))
            self.textBox.config(fg=("#"+fcs.rOA(self.stickies).colors["text"]))
            self.textBox.config(insertbackground=("#"+fcs.rOA(self.stickies).colors["text"]))

class Sticky:
    def __init__(self, filePath, title, theme, content):
        self.filePath = filePath
        self.title = title
        self.theme = theme
        self.content = content
        self.active = False
        self.colors = {
            "main": None,
            "alt1": None,
            "alt2": None,
            "text": None
        }
        self.resetColors()
    
    def __str__(self):
        return ("Sticky of title: " + self.title + "\n  with file path: " + self.filePath + "\n  with active state: " + str(self.active) + "\n  with content: " + self.content)

    # adding save functions right into the sticky info object
    def save(self):
        toWrite = "/TITLE " + self.title + "\n/THEME " + self.theme + "\n/START-CONTENT\n" + self.content + "/END-CONTENT\n"
        f = open(self.filePath, "wt")
        f.write(toWrite)
        f.close()

    def setText(self, newContent):  # kinda redundant tho, but whatever...
        self.content = newContent
    
    def resetColors(self):
        self.colors = fcs.makeColorDict(self.theme)
