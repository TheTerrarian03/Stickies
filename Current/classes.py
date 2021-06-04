from os import remove
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import functions as fcs
import os

class MainWindow:
    def __init__(self, master, version):
        self.fullscreen = False
        self.version = version
        self.master = master
        self.setWindowTitle()
        self.chosenTheme = StringVar()
        self.showLineNumbers = BooleanVar()
        if fcs.getOS() == "macOS":
            self.osName = "mac"
        else:
            self.osName = "pc"

        ### sticky objects and stuff
        self.stickies = fcs.getAllStickies()
        if fcs.getLastOpen():
            try:
                self.stickies = fcs.setNewActive(self.stickies, fcs.getLastOpen())
            except AttributeError:
                self.stickies[0].active = True
                print("except")
        else:
            self.stickies[0].active = True

        # text box for entering info
        self.textBox = Text(master)
        self.textBox.pack(side=LEFT, expand=True, fill='both')

        # textbox scrollbar
        self.scrollb = Scrollbar(master, command=self.textBox.yview, width=12)
        self.scrollb.pack(side=RIGHT, fill=Y)
        self.textBox['yscrollcommand'] = self.scrollb.set

        ### menu bar
        # main top menu
        self.menu = Menu(master)
        master.config(menu=self.menu)
        # file sub-menu
        self.fileMenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.fileMenu)
        if self.osName == "mac":
            self.fileMenu.add_command(label="New Sticky", accelerator="CMD-N", command=self.newSticky)
            self.fileMenu.add_command(label="Open", accelerator="CMD-O", command=self.loadStickies)
            self.fileMenu.add_separator()
            self.fileMenu.add_command(label="Save Sticky", accelerator="CMD-S", command=self.saveActiveSticky)
        elif self.osName == "pc":
            self.fileMenu.add_command(label="New Sticky", accelerator="CTRL-N", command=self.newSticky)
            self.fileMenu.add_command(label="Open", accelerator="CTRL-O", command=self.loadStickies)
            self.fileMenu.add_separator()
            self.fileMenu.add_command(label="Save Sticky", accelerator="CTRL-S", command=self.saveActiveSticky)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.exitWindow)
        # edit sub-menu
        self.editMenu = Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.editMenu)
        if self.osName == "mac":
            self.editMenu.add_command(label="Undo", accelerator="CMD-Z", state=DISABLED)
            self.editMenu.add_command(label="Redo", accelerator="CMD-Shift-Z", state=DISABLED)
        elif self.osName == "pc":
            self.editMenu.add_command(label="Undo", accelerator="CTRL-Z", state=DISABLED)
            self.editMenu.add_command(label="Redo", accelerator="CTRL-Shift-Z", state=DISABLED)
        self.editMenu.add_command(label="Sorry, there is no Undo or Redo...\n   >:D", state=DISABLED)
        self.editMenu.add_separator()
        if self.osName == "mac":
            self.editMenu.add_command(label="Select all", accelerator="CMD-A", command=lambda: self.master.focus_get().event_generate("<Command-a>"))
            self.editMenu.add_separator()
            self.editMenu.add_command(label="Cut", accelerator="CMD-X", command=lambda: self.master.focus_get().event_generate("<<Cut>>"))
            self.editMenu.add_command(label="Copy", accelerator="CMD-C", command=lambda: self.master.focus_get().event_generate("<<Copy>>"))
            self.editMenu.add_command(label="Paste", accelerator="CMD-V", command=lambda: self.master.focus_get().event_generate("<<Paste>>"))
        elif self.osName == "pc":
            self.editMenu.add_command(label="Select all", accelerator="CMD-A", command=lambda: self.master.focus_get().event_generate("<Command-a>"))
            self.editMenu.add_separator()
            self.editMenu.add_command(label="Cut", accelerator="CTRL-X", command=lambda: self.master.focus_get().event_generate("<<Cut>>"))
            self.editMenu.add_command(label="Copy", accelerator="CTRL-C", command=lambda: self.master.focus_get().event_generate("<<Copy>>"))
            self.editMenu.add_command(label="Paste", accelerator="CTRL-V", command=lambda: self.master.focus_get().event_generate("<<Paste>>"))
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Clear Sticky", command=self.clearSticky)
        self.editMenu.add_command(label="Delete Sticky", command=self.deleteSticky)
        self.editMenu.add_separator()
        self.editMenu.add_command(label="All To Lowercase", command=self.allToLowercase)
        self.editMenu.add_command(label="All To Uppercase", command=self.allToUppercase)
        self.editMenu.add_command(label="To Chaos. Don't do it. Please.", command=self.allToChaos)
        # theme sub-menu
        self.themeMenu = Menu(self.menu)
        self.menu.add_cascade(label="Theme", menu=self.themeMenu)
        self.themeMenu.add_radiobutton(label="Yellow", variable=self.chosenTheme, value="YELLOW", command=self.changeTheme)
        self.themeMenu.add_radiobutton(label="Orange", variable=self.chosenTheme, value="ORANGE", command=self.changeTheme)
        self.themeMenu.add_radiobutton(label="Pink", variable=self.chosenTheme, value="PINK", command=self.changeTheme)
        self.themeMenu.add_radiobutton(label="Purple", variable=self.chosenTheme, value="PURPLE", command=self.changeTheme)
        self.themeMenu.add_radiobutton(label="Green", variable=self.chosenTheme, value="GREEN", command=self.changeTheme)
        self.themeMenu.add_radiobutton(label="Blue", variable=self.chosenTheme, value="BLUE", command=self.changeTheme)
        self.themeMenu.add_radiobutton(label="Dark", variable=self.chosenTheme, value="DARK", command=self.changeTheme)
        self.themeMenu.add_radiobutton(label="Light", variable=self.chosenTheme, value="LIGHT", command=self.changeTheme)
        # title sub-menu
        self.titleMenu = Menu(self.menu)
        self.menu.add_cascade(label="Title", menu=self.titleMenu)
        self.titleMenu.add_command(label="Choose new Title", command=self.chooseNewTitle)
        self.titleMenu.add_command(label="Clear Title to Default", command=self.clearTitleToDefault)
        # window sub-menu
        self.windowMenu = Menu(self.menu)
        self.menu.add_cascade(label="Window", menu=self.windowMenu)
        if self.osName == "mac":
            self.fullscreenMenu = self.windowMenu.add_command(label="Go Fullscreen", accelerator="CMD-F", command=self.switchFullscreen)
        elif self.osName == "pc":
            self.fullscreenMenu = self.windowMenu.add_command(label="Go Fullscreen", accelerator="CTRL-F", command=self.switchFullscreen)
        self.windowMenu.add_command(label="Auto Resize", command=self.fillerFunction, state=DISABLED)
        self.windowMenu.add_separator()
        if self.osName == "mac":
            self.windowMenu.add_command(label="Reload", accelerator="CMD-R", command=self.fillerFunction, state=DISABLED)
        elif self.osName == "pc":
            self.windowMenu.add_command(label="Reload", accelerator="CTRL-R", command=self.fillerFunction, state=DISABLED)
        self.windowMenu.add_radiobutton(label="Show Line Numbers", command=self.fillerFunction)
        # help command in main menu
        self.helpMenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(label="Get Help", command=self.fillerFunction, state=DISABLED)
        self.helpMenu.add_command(label="About Stickies", command=self.fillerFunction, state=DISABLED)
        # bind all stuff for hotkeys and keybaord shortcuts
        if self.osName == "mac":
            self.master.bind_all("<Command-o>", self.loadStickies)
            self.master.bind_all("<Command-n>", self.newSticky)
            self.master.bind_all("<Command-s>", self.saveActiveSticky)
            self.master.bind_all("<Command-f>", self.switchFullscreen)
        elif self.osName == "pc":
            self.master.bind_all("<Command-o>", self.loadStickies)
            self.master.bind_all("<Command-n>", self.newSticky)
            self.master.bind_all("<Command-s>", self.saveActiveSticky)
            self.master.bind_all("<Command-f>", self.switchFullscreen)

        ### call the reset function
        self.resetWidgets()
        self.setWindowTitle(stickyTitle=fcs.rOA(self.stickies).title)
    
    ### Menu functions (in order of command added)
    def newSticky(self, event=None):
        print("Making new Sticky")
        newStickyTitle = fcs.makeNewSticky(returnTitle=True)
        self.saveActiveSticky()
        self.stickies = fcs.getAllStickies()
        self.stickies = fcs.setNewActive(self.stickies, newStickyTitle)
        self.resetWidgets()
        fcs.setLastOpen(fcs.rOA(self.stickies).title)
        self.setWindowTitle(stickyTitle=fcs.rOA(self.stickies).title)
        print("Finished making new Sticky")

    def loadStickies(self, event=None):
        print("Loading Stickies...")
        filetypes = (("Sticky Saves", ".sticky"), ("All Files", "*.*"))
        chosenPath = tkinter.filedialog.askopenfilename(title='Open a file', initialdir=os.curdir+"/SAVES", filetypes=filetypes)
        if chosenPath:
            chosenStickyPath = chosenPath.split("/")[-2]+"/"+chosenPath.split("/")[-1]
            self.stickies = fcs.setNewActive(self.stickies, fcs.returnObjWithSamePath(self.stickies, chosenStickyPath).title)
            self.resetWidgets()
            fcs.setLastOpen(fcs.returnObjWithSamePath(self.stickies, chosenStickyPath).title)
            self.setWindowTitle(stickyTitle=fcs.rOA(self.stickies).title)

    def saveActiveSticky(self, event=None):
        print("Saving Sticky with title: " + fcs.rOA(self.stickies).title)
        fcs.rOA(self.stickies).setText(self.textBox.get("1.0", "end"))
        fcs.rOA(self.stickies).save()
        fcs.setLastOpen(fcs.rOA(self.stickies).title)
        print("Done Saving Sticky.")

    def exitWindow(self, event=None):
        title = "Exit Stickies v"+str(self.version)
        exitConfirm = tkinter.messagebox.askyesno(title, "Are you sure you want to quit?")
        if exitConfirm:
            quit()
    
    def clearSticky(self, event=None):
        fcs.rOA(self.stickies).content = "Silence."
        self.resetWidgets(setColors=False)
    
    def deleteSticky(self, event=None):
        confirm = tkinter.messagebox.askyesno("Delete Sticky", "Are you sure you want to delete this Sticky?\n("+fcs.rOA(self.stickies).title+")")
        if confirm:
            fcs.deleteFile(fcs.rOA(self.stickies).filePath)
            self.stickies = fcs.getAllStickies()
            self.stickies[0].active = True
            self.resetWidgets()
            fcs.setLastOpen(fcs.returnOnlyActive(self.stickies).title)
            self.setWindowTitle(fcs.returnOnlyActive(self.stickies).title)
        else:
            tkinter.messagebox.showinfo("Delete Sticky", "Good job. Always keep you problems until you solve them. Keep and control them!")
    
    def allToLowercase(self, event=None):
        self.saveActiveSticky()
        fcs.rOA(self.stickies).content = fcs.rOA(self.stickies).content.lower()
        self.resetWidgets(setColors=False)
    
    def allToUppercase(self, event=None):
        self.saveActiveSticky()
        fcs.rOA(self.stickies).content = fcs.rOA(self.stickies).content.upper()
        self.resetWidgets(setColors=False)
    
    def allToChaos(self, event=None):
        self.saveActiveSticky()
        confirm = tkinter.messagebox.askyesno("Convert All Text To Chaos", "Are you REALLY sure you want to do this?\nI don't think it's a good idea...")
        if confirm:
            fcs.rOA(self.stickies).content = fcs.toUpperAndLowerAlternating(fcs.rOA(self.stickies).content)
            self.resetWidgets(setColors=False)
            tkinter.messagebox.showinfo("Convert All Text To Chaos", "I hope you enjoy what you've done.\n>:(")
        else:
            tkinter.messagebox.showinfo("Conver All Text To Chaos", "Good choice!\n:D")
    
    def changeTheme(self, event=None):
        fcs.rOA(self.stickies).theme = self.chosenTheme.get()
        self.saveActiveSticky()
        oldTitle = fcs.rOA(self.stickies).title
        self.stickies = fcs.getAllStickies()
        self.stickies = fcs.setNewActive(self.stickies, oldTitle)
        fcs.setLastOpen(fcs.rOA(self.stickies).title)
        self.setWindowTitle(stickyTitle=fcs.rOA(self.stickies).title)
        self.resetWidgets()
    
    def chooseNewTitle(self, event=None):
        newTitle = None
        self.titlePopup = popupWindow(self.master, "What is your new title? Enter here:")
        self.master.wait_window(self.titlePopup.top)
        newTitle = self.titlePopup.value

        fcs.rOA(self.stickies).title = newTitle
        self.saveActiveSticky()

        fcs.renameSticky(fcs.rOA(self.stickies).filePath, newTitle)
        self.stickies = fcs.getAllStickies()
        self.stickies = fcs.setNewActive(self.stickies, newTitle)

        self.setWindowTitle(stickyTitle=fcs.rOA(self.stickies).title)

        fcs.setLastOpen(newTitle)

    def clearTitleToDefault(self, event=None):
        newTitle = fcs.makeNewSticky(returnTitle=True, makeSave=False)

        fcs.rOA(self.stickies).title = newTitle
        self.saveActiveSticky()

        fcs.renameSticky(fcs.rOA(self.stickies).filePath, newTitle)
        self.stickies = fcs.getAllStickies()
        self.stickies = fcs.setNewActive(self.stickies, newTitle)

        self.setWindowTitle(stickyTitle=fcs.rOA(self.stickies).title)

        fcs.setLastOpen(newTitle)
     
    def switchFullscreen(self, event=None):
        if self.fullscreen:
            self.fullscreen = False
            self.master.attributes("-fullscreen", False)
            self.windowMenu.entryconfigure(0, label="Go Fullscreen")
        else:
            self.fullscreen = True
            self.master.attributes("-fullscreen", True)
            self.windowMenu.entryconfigure(0, label="Exit Fullscreen")

    ### Other functions
    def fillerFunction(self):
        print("Unfortunately, this button hasn't been assigned any functionality yet. :(")
        tkinter.messagebox.showerror("ERROR! No Functionality Has Been Added!", "Unfortunately, this button hasn't been assigned any functionality yet.\n:(")

    def setWindowTitle(self, stickyTitle=""):
        newTitle = "Stickies v"+str(self.version)+" - "+stickyTitle if stickyTitle else "Stickies v"+str(self.version)
        self.master.title(newTitle)

    def resetWidgets(self, setText=True, setColors=True):
        # theme radio button
        self.chosenTheme.set(fcs.rOA(self.stickies).theme)
        # setting text
        if setText:
            # delete first
            self.textBox.delete("0.0", "end")
            # then insert needed text
            try:
                newContent = fcs.rOA(self.stickies).content
            except AttributeError:
                self.stickies = fcs.getAllStickies()
                self.stickies[0].active = True
                fcs.setLastOpen(fcs.rOA(self.stickies).title)
                tkinter.messagebox.showwarning("Error Load Last Used Sticky Note", "It seems the sticky note you last had open has been deleted, so we opened the first one we saw in the folder instead.")
            newContent = fcs.rOA(self.stickies).content
            if newContent.endswith("\n"):
                newContent = newContent[:-1]
            self.textBox.insert("0.0", newContent)
        # setting colors
        if setColors:
            self.textBox.config(bg=("#"+fcs.rOA(self.stickies).colors["main"]))
            self.textBox.config(fg=("#"+fcs.rOA(self.stickies).colors["text"]))
            self.textBox.config(insertbackground=("#"+fcs.rOA(self.stickies).colors["text"]))

class popupWindow:
    def __init__(self, master, question, icon=None):
        # variable
        self.value = None
        # widgets and window making + setup
        self.top = Toplevel(master)
        self.label = Label(self.top, text=question)
        self.label.pack(side=TOP, fill=X)
        self.entry = Entry(self.top)
        self.entry.pack(side=TOP)
        self.button = Button(self.top, text="Submit", command=self.submit)
        self.button.pack(side=TOP)
    
    def submit(self, event=None):
        self.value = self.entry.get()
        self.top.destroy()

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
