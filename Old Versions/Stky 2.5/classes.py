from os import remove
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import functions as fcs
import os

class MainWindow:
    def __init__(self, master, version):
        # initial variables needed later
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

        ### menu bar example
        """
        # main top-menu
        self.exMainMenu = Menu(master)
        master.config(menu=self.exMainMenu)
        # example menu
        self.exSmallerMenu = Menu(self.exMainMenu)
        self.exMainMenu.add_cascade(label="Example Smaller Menu", menu=self.exSmallerMenu)
        self.exSmallerMenu.add_command(label="Example Command", accelerator="CMD-E", command=self.command)
        """

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
            self.fileMenu.add_command(label="Open Default", accelerator="CMD-W", command=self.openDefault)
            self.fileMenu.add_separator()
            self.fileMenu.add_command(label="Save Sticky", accelerator="CMD-S", command=self.saveActiveSticky)
        elif self.osName == "pc":
            self.fileMenu.add_command(label="New Sticky", accelerator="CTRL-N", command=self.newSticky)
            self.fileMenu.add_command(label="Open", accelerator="CTRL-O", command=self.loadStickies)
            self.fileMenu.add_command(label="Open Default", accelerator="CTRL-W", command=self.openDefault)
            self.fileMenu.add_separator()
            self.fileMenu.add_command(label="Save Sticky", accelerator="CTRL-S", command=self.saveActiveSticky)
        self.fileMenu.add_command(label="Delete Sticky", command=self.deleteSticky)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.exitWindow)
        # edit sub-menu
        self.editMenu = Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.editMenu)
        if self.osName == "mac":
            self.editMenu.add_command(label="Undo", accelerator="CMD-Z", state=DISABLED)
            self.editMenu.add_command(label="Redo", accelerator="CMD-Shift-Z", state=DISABLED)
        elif self.osName == "pc":
            self.editMenu.add_command(label="Undo", accelerator="Ctrl-Z", state=DISABLED)
            self.editMenu.add_command(label="Redo", accelerator="Ctrl-Shift-Z", state=DISABLED)
        self.editMenu.add_command(label="Sorry, there is no Undo or Redo...\n   >:D", state=DISABLED)
        self.editMenu.add_separator()
        if self.osName == "mac":
            self.editMenu.add_command(label="Select all", accelerator="CMD-A", command=lambda: self.master.focus_get().event_generate("<Command-a>"))
            self.editMenu.add_separator()
            self.editMenu.add_command(label="Cut", accelerator="CMD-X", command=lambda: self.master.focus_get().event_generate("<<Cut>>"))
            self.editMenu.add_command(label="Copy", accelerator="CMD-C", command=lambda: self.master.focus_get().event_generate("<<Copy>>"))
            self.editMenu.add_command(label="Paste", accelerator="CMD-V", command=lambda: self.master.focus_get().event_generate("<<Paste>>"))
        elif self.osName == "pc":
            self.editMenu.add_command(label="Select all", accelerator="Ctrl-A", command=lambda: self.master.focus_get().event_generate("<Command-a>"))
            self.editMenu.add_separator()
            self.editMenu.add_command(label="Cut", accelerator="Ctrl-X", command=lambda: self.master.focus_get().event_generate("<<Cut>>"))
            self.editMenu.add_command(label="Copy", accelerator="Ctrl-C", command=lambda: self.master.focus_get().event_generate("<<Copy>>"))
            self.editMenu.add_command(label="Paste", accelerator="Ctrl-V", command=lambda: self.master.focus_get().event_generate("<<Paste>>"))
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Clear Sticky", command=self.clearSticky)
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
            self.windowMenu.add_command(label="Reload", accelerator="Ctrl-R", command=self.fillerFunction, state=DISABLED)
        # help command in main menu
        self.helpMenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(label="Get Help", command=self.fillerFunction, state=DISABLED)
        self.helpMenu.add_command(label="About Stickies", command=self.fillerFunction, state=DISABLED)
        # bind all stuff for hotkeys and keybaord shortcuts
        if self.osName == "mac":
            self.master.bind_all("<Command-o>", self.loadStickies)
            self.master.bind_all("<Command-n>", self.newSticky)
            self.master.bind_all("<Command-w>", self.openDefault)
            self.master.bind_all("<Command-s>", self.saveActiveSticky)
            self.master.bind_all("<Command-f>", self.switchFullscreen)
        elif self.osName == "pc":
            self.master.bind_all("<Ctrl-o>", self.loadStickies)
            self.master.bind_all("<Ctrl-n>", self.newSticky)
            self.master.bind_all("<Ctrl-w>", self.openDefault)
            self.master.bind_all("<Command-f>", self.switchFullscreen)
            self.master.bind_all("<Ctrl-s>", self.saveActiveSticky)

        ### reset widgets and set the window title
        self.resetWidgets()
        self.setWindowTitle(stickyTitle=fcs.rOA(self.stickies).title)

        # confirm closing
        self.master.protocol("WM_DELETE_WINDOW", self.exitWindow)
    
    ### Menu functions (in order of command added)
    def newSticky(self, event=None):
        # make sure the user saves if they want to
        if self.isSaved():
            # make a sticky save
            newStickyTitle = fcs.makeNewSticky(returnTitle=True)
            # save the sticky now, set active, reset widgets, set last open, and window title
            self.saveActiveSticky()
            self.stickies = fcs.getAllStickies()
            self.stickies = fcs.setNewActive(self.stickies, newStickyTitle)
            self.resetWidgets()
            fcs.setLastOpen(fcs.rOA(self.stickies).title)
            self.setWindowTitle(stickyTitle=fcs.rOA(self.stickies).title)

    def loadStickies(self, event=None):
        # some stuff for tkinter about file types
        filetypes = (("Sticky Saves", ".sticky"), ("All Files", "*.*"))
        # make sure user saves sticky if needed
        if self.isSaved():
            # choose file and set path to variable
            chosenPath = tkinter.filedialog.askopenfilename(title='Open a file', initialdir=os.curdir+"/SAVES", filetypes=filetypes)
            # if a file is chosen, then:
            if chosenPath:
                # yes
                chosenStickyPath = chosenPath.split("/")[-2]+"/"+chosenPath.split("/")[-1]
                # set new active, reset widgets, set last open, and set window title
                self.stickies = fcs.setNewActive(self.stickies, fcs.returnObjWithSamePath(self.stickies, chosenStickyPath).title)
                self.commonReset()
            
    def openDefault(self, event=None):
        # make sure user saves if they need to
        if self.isSaved():
            # get stickies, reset widgets, set last open, and set window title
            self.stickies = fcs.getAllStickies()
            self.stickies[0].active = True
            self.commonReset()

    def saveActiveSticky(self, event=None):
        # set text from the textbox on the window
        fcs.rOA(self.stickies).setText(self.textBox.get("1.0", "end"))
        # save it!
        fcs.rOA(self.stickies).save()
        # set lsat open because otherwise problems occur sometimes
        fcs.setLastOpen(fcs.rOA(self.stickies).title)

    def exitWindow(self, event=None):
        # confirm whether the user wants to or not
        title = "Exit Stickies v"+str(self.version)
        exitConfirm = tkinter.messagebox.askyesno(title, "Are you sure you want to quit?")
        # if they say yes, then quit.
        if exitConfirm:
            quit()
    
    def clearSticky(self, event=None):
        # set contnet
        fcs.rOA(self.stickies).content = "Silence."
        # reset widgets (in this case, set the text box title)
        self.resetWidgets()
    
    def deleteSticky(self, event=None):
        # do they REALLY WANT TO?!
        confirm = tkinter.messagebox.askyesno("Delete Sticky", "Are you sure you want to delete this Sticky?\n("+fcs.rOA(self.stickies).title+")")
        # if they do
        if confirm:
            # delete the file
            fcs.deleteFile(fcs.rOA(self.stickies).filePath)
            # ... stuff ... I've told you what this does before!
            self.stickies = fcs.getAllStickies()
            self.stickies[0].active = True
            self.resetWidgets()
            fcs.setLastOpen(fcs.returnOnlyActive(self.stickies).title)
            self.setWindowTitle(fcs.returnOnlyActive(self.stickies).title)
        # fill them with guilt even though they chose the right option
        else:
            tkinter.messagebox.showinfo("Delete Sticky", "Good job. Always keep you problems until you solve them. Keep and control them!")
    
    def allToLowercase(self, event=None):
        # save, because I don't have Undo + Redo working yet
        self.saveActiveSticky()
        # set content
        fcs.rOA(self.stickies).content = fcs.rOA(self.stickies).content.lower()
        # reset widgets (in this case, set the text box title)
        self.resetWidgets()
    
    def allToUppercase(self, event=None):
        # save, because I don't have Unfo + Redo working yet
        self.saveActiveSticky()
        # set content
        fcs.rOA(self.stickies).content = fcs.rOA(self.stickies).content.upper()
        # reset widgets (in this case, set the text box title)
        self.resetWidgets(setColors=False)
    
    def allToChaos(self, event=None):
        # save, because I don't have Unfo + Redo working yet
        self.saveActiveSticky()
        # do they really want to?
        confirm = tkinter.messagebox.askyesno("Convert All Text To Chaos", "Are you REALLY sure you want to do this?\nI don't think it's a good idea...")
        # if they do, then set content, then reset widgets
        if confirm:
            fcs.rOA(self.stickies).content = fcs.toUpperAndLowerAlternating(fcs.rOA(self.stickies).content)
            self.resetWidgets(setColors=False)
            # guilt.
            tkinter.messagebox.showinfo("Convert All Text To Chaos", "I hope you enjoy what you've done.\n>:(")
        else:
            # encourage not picking yes
            tkinter.messagebox.showinfo("Conver All Text To Chaos", "Good choice!\n:D")
    
    def changeTheme(self, event=None):
        # change the theme based on what's chosen
        fcs.rOA(self.stickies).theme = self.chosenTheme.get()
        # save sitcky
        self.saveActiveSticky()
        # get the old title for setting active later
        oldTitle = fcs.rOA(self.stickies).title
        # get sticky saves
        self.stickies = fcs.getAllStickies()
        # set active (which will be what was open before)
        self.stickies = fcs.setNewActive(self.stickies, oldTitle)
        # set last open, since otherwise some problems will pop up
        fcs.setLastOpen(fcs.rOA(self.stickies).title)
        # set window title and reset widgets, including colors of window items
        self.setWindowTitle(stickyTitle=fcs.rOA(self.stickies).title)
        self.resetWidgets()
    
    def popupSetTitle(self, newTitle, event=None):
        print("popupSetTitle Called")
        # set the title
        fcs.rOA(self.stickies).title = newTitle
        # save sticky
        self.saveActiveSticky()
        # rename, get stickies, set new active, set window title, and set last open
        fcs.renameSticky(fcs.rOA(self.stickies).filePath, newTitle)
        self.stickies = fcs.getAllStickies()
        self.stickies = fcs.setNewActive(self.stickies, newTitle)
        self.setWindowTitle(stickyTitle=fcs.rOA(self.stickies).title)
        fcs.setLastOpen(newTitle)

    def chooseNewTitle(self, event=None):
        # these 2 lines make a popup window and set 'newTitle' to what the user enters in the popup window's entry box
        self.titlePopup = popupWindow(self.master, "What is your new title? Enter here:", self.popupSetTitle)
        print(fcs.rOA(self.stickies).title)

    def clearTitleToDefault(self, event=None):
        # set 'newTitle' to the next-available default title
        newTitle = fcs.makeNewSticky(returnTitle=True, makeSave=False)
        # set title and save
        fcs.rOA(self.stickies).title = newTitle
        self.saveActiveSticky()
        # rename, get stickies, set new active, set window title, and set last open
        fcs.renameSticky(fcs.rOA(self.stickies).filePath, newTitle)
        self.stickies = fcs.getAllStickies()
        self.stickies = fcs.setNewActive(self.stickies, newTitle)
        self.setWindowTitle(stickyTitle=fcs.rOA(self.stickies).title)
        fcs.setLastOpen(newTitle)
     
    def switchFullscreen(self, event=None):
        # if the window is fullscreen
        if self.fullscreen:
            # set the value, make the window fullscreen, and set the entry in the window menu
            self.fullscreen = False
            self.master.attributes("-fullscreen", False)
            self.windowMenu.entryconfigure(0, label="Go Fullscreen")
        # if not fullscreen
        else:
            # set the value, make the window fullscreen, and set the entry in the window menu
            self.fullscreen = True
            self.master.attributes("-fullscreen", True)
            self.windowMenu.entryconfigure(0, label="Exit Fullscreen")

    ### Other functions
    def fillerFunction(self):
        # print and show message
        print("Unfortunately, this button hasn't been assigned any functionality yet. :(")
        tkinter.messagebox.showerror("ERROR! No Functionality Has Been Added!", "Unfortunately, this button hasn't been assigned any functionality yet.\n:(")

    def setWindowTitle(self, stickyTitle=""):
        # set a variable to a title
        newTitle = "Stky v"+str(self.version)+" - "+stickyTitle if stickyTitle else "Stky v"+str(self.version)
        # y'know... set the title
        self.master.title(newTitle)

    def isSaved(self, event=None, preset="You have't saved your Sticky yet. "):
        if self.textBox.get("0.0", "end") == fcs.rOA(self.stickies).content:
            return True
        else:
            saveNow = tkinter.messagebox.askyesnocancel("Save Sticky?", preset+"Do you want to save before continuing?")
            if saveNow == True:
                self.saveActiveSticky()
                return True
            elif saveNow == False:
                return True
            else:
                return False

    def commonReset(self, event=None):
        # reset widgets
        self.resetWidgets()
        # set the last open for next time
        fcs.setLastOpen(fcs.rOA(self.stickies).title)
        # set the window title to match
        self.setWindowTitle(stickyTitle=fcs.rOA(self.stickies).title)

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
            # textbox background and text colors
            self.textBox.config(bg=("#"+fcs.rOA(self.stickies).colors["main"]))
            self.textBox.config(fg=("#"+fcs.rOA(self.stickies).colors["text"]))
            # cursor color, same as text color
            self.textBox.config(insertbackground=("#"+fcs.rOA(self.stickies).colors["text"]))

class popupWindow:
    def __init__(self, master, question, submitFunc, icon=None):
        # variable
        self.value = None
        # fucnction to call
        self.submitFunc = submitFunc
        # widgets and window making + setup
        self.top = Toplevel(master)
        self.label = Label(self.top, text=question)
        self.label.pack(side=TOP, fill=X)
        self.entry = Entry(self.top)
        self.entry.pack(side=TOP)
        self.button = Button(self.top, text="Submit", command=self.submit)
        self.button.pack(side=TOP)
        # debugging
        print("popupWindow created")
    
    def submit(self, event=None):
        print("Popup submit called")
        self.value = self.entry.get()
        self.submitFunc(self.value)
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
