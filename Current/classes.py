import pygame
import functions as fcs
import PygameTextWriter as pTW
import PygameKeyTracker as pKT

class toggleableImg:
  def __init__(self, name, pos, margins, imgPaths, function, value=False):
    # imgPaths must be a list of two paths
    # first image is for off, second for on
    self.name = name
    self.pos = pos
    self.margins = margins
    self.imgs = []
    for i in imgPaths:
      self.imgs.append(pygame.image.load(i))
    self.value = value
    self.func = function
    self.res = (self.imgs[0].get_rect()[2], self.imgs[0].get_rect()[3])
  
  def collide(self, mPos, autoCall=False):
    if (self.pos[0] <= mPos[0] <= self.pos[0]+self.res[0]) and (self.pos[1] <= mPos[1] <= self.pos[1]+self.res[1]):
      if autoCall:
        self.value = fcs.flip(self.value)
        self.func(self.value)
        print(self.name + "-s value: " + str(self.value))
      else:
        return True
    return False
  
  def draw(self, dispSurface):
    if self.value:
      dispSurface.blit(self.imgs[1], (self.pos[0]+self.margins[0], self.pos[1]+self.margins[1]))
    else:
      dispSurface.blit(self.imgs[0], (self.pos[0]+self.margins[0], self.pos[1]+self.margins[1]))

class clickableRect:
  def __init__(self, name, pos, res, mainColor, borderColor, margins, function, scale=1):
    self.name = name
    self.pos = pos
    self.res = (res[0]*scale, res[1]*scale)
    self.mC = mainColor
    self.bC = borderColor
    self.margins = (margins[0]*scale, margins[1]*scale)
    self.func = function
  
  def collide(self, mPos, autoCall=False):
    if (self.pos[0] <= mPos[0] <= self.pos[0]+self.res[0]) and (self.pos[1] <= mPos[1] <= self.pos[1]+self.res[1]):
      if autoCall:
        self.func(self.name)
      else:
        return True
    return False
  
  def draw(self, dispSurface):
    pygame.draw.rect(dispSurface, self.bC, (self.pos[0]+self.margins[0], self.pos[1]+self.margins[1], self.res[0], self.res[1]))  # border
    pygame.draw.rect(dispSurface, self.mC, (self.pos[0]+2+self.margins[0], self.pos[1]+2+self.margins[1], self.res[0]-4, self.res[1]-4))  # inside

class icon:
  def __init__(self, name, pos, iconPath, margins, function, scale=1):
    self.name = name
    self.img = pygame.image.load(iconPath)
    self.img = pygame.transform.scale(self.img, (int(self.img.get_rect()[2]*scale), int(self.img.get_rect()[3]*scale)))
    self.margins = [margins[0]*scale, margins[1]*scale]
    self.func = function
    self.pos = [pos[0]*scale, pos[1]*scale]
    self.res = (self.img.get_rect()[2], self.img.get_rect()[3])
    print(self.res)
  
  def collide(self, mPos, autoCall=False):
    if (self.pos[0] <= mPos[0] <= self.pos[0]+self.res[0]) and (self.pos[1] <= mPos[1] <= self.pos[1]+self.res[1]):
      if autoCall:
        self.func()
      else:
        return True
    return False
  
  def draw(self, dispSurface, border=True, borderColor=(0, 0, 0)):
    dispSurface.blit(self.img, self.pos)
    if border and self.collide(pygame.mouse.get_pos()):
      pygame.draw.rect(dispSurface, borderColor, (self.pos[0]-self.margins[0], self.pos[1]-self.margins[1], self.res[0]+self.margins[0]*2, 1))  # top-left -> right
      pygame.draw.rect(dispSurface, borderColor, (self.pos[0]-self.margins[0], self.pos[1]-self.margins[0], 1, self.res[1]+self.margins[1]*2))  # top-left -> down
      pygame.draw.rect(dispSurface, borderColor, (self.pos[0]-self.margins[0], self.pos[1]+self.res[1]+self.margins[1]-1, self.res[0]+self.margins[0]*2, 1))  # bottom-left -> right
      pygame.draw.rect(dispSurface, borderColor, (self.pos[0]+self.res[0]+self.margins[0], self.pos[1]-self.margins[1], 1, self.res[1]+self.margins[1]*2))  # top-right -> down
  
  def move(self, newPos):
    self.pos = newPos

class stickySave:
  def __init__(self, pos, res, margins, stickyObj, function):
    self.pos = pos
    self.res = res
    self.margins = margins
    self.stickyObj = stickyObj
    self.title = stickyObj.title
    self.func = function
  
  def collide(self, mPos, autoCall=False):
    if (self.pos[0] <= mPos[0] <= self.pos[0]+self.res[0]) and (self.pos[1] <= mPos[1] <= self.pos[1]+self.res[1]):
      if autoCall:
        self.func(self.title)
      else:
        return True
    return False
  
  def draw(self, dispSurface, pTW):
    pygame.draw.rect(dispSurface, self.stickyObj.mainColor, (self.pos[0], self.pos[1], self.res[0], self.res[1]))
    pTW.write(self.title, [self.pos[0]+self.margins[0], self.pos[1]+self.margins[1]])
    if self.collide(pygame.mouse.get_pos()):
      pygame.draw.rect(dispSurface, self.stickyObj.altColor1, (self.pos[0], self.pos[1], self.res[0], 1))  # top-left -> right
      pygame.draw.rect(dispSurface, self.stickyObj.altColor1, (self.pos[0], self.pos[1], 1, self.res[1]))  # top-left -> bottom
      pygame.draw.rect(dispSurface, self.stickyObj.altColor1, (self.pos[0], self.pos[1]+self.res[1], self.res[0], 1))  # bottom-left -> right
      pygame.draw.rect(dispSurface, self.stickyObj.altColor1, (self.pos[0]+self.res[0], self.pos[1], 1, self.res[1]))  # top-right -> down

#======================#
#----- INFO CLASS -----#
#======================#

class Info:
  def __init__(self, fps=30):
    self.stickies = self.loadStickies()
    self.dispObj = None
    self.keyTracker = None
    self.textWriter = None # pTW.TextWriter(self.dispObj.surface, (0, 0, 0))
    self.clock = pygame.time.Clock()
    self.fps = fps
    # initializing function calls
    self.setDispObj()
    self.setTextWriter()    
    self.reset()
  
  def setDispObj(self):
    self.dispObj = graphicalContainer((500, 350), fcs.rOA(self.stickies).mainColor, fcs.rOA(self.stickies).altColor1)
  
  def setTextWriter(self):
    self.textWriter = pTW.TextWriter(self.dispObj.surface, (0, 0, 0))

  def reset(self):
    # reset icon positions, set the key tracker, and set the window caption
    fcs.rOA(self.stickies).resetIconPositions()
    fcs.rOA(self.stickies).checkMargins()
    self.keyTracker = pKT.KeyTracker(fcs.rOA(self.stickies).add, fcs.rOA(self.stickies).backspace, fcs.rOA(self.stickies).directionHandle, fps=self.fps)
    pygame.display.set_caption(fcs.rOA(self.stickies).title)

  def loadStickies(self):
    fcsLoadedStickies = fcs.loadStickies()
    stickies = []
    for i in fcsLoadedStickies:
      stickies.append(Sticky(self, i))
    stickies[0].active = True
    self.stickies = stickies
    return stickies
    # reset()
    # keyTracker = pKT.KeyTracker(fcs.rOA(stickies).add, fcs.rOA(stickies).backspace, fcs.rOA(stickies).directionHandle, fps=fps)
  
  def changeActive(self, title):
    fcs.rOA(self.stickies).menu = "CONTENT"
    for sticky in self.stickies:
      sticky.active = False
    for sticky in self.stickies:
      if sticky.title == title:
        sticky.active = True
        sticky.menu = "CONTENT"
    self.reset()

#========================#
#----- STICKY CLASS -----#
#========================#

ICON_ORDER = ["SAVE", "OPEN", "NEW", "SETTINGS", "ZOOM-PLUS", "ZOOM-MINUS"]

class Sticky:
  def __init__(self, infoObj, attrDict, cursorPos=None):
    # functions from main file
    self.infoObj = infoObj
    # set info from attrDict
    self.title = attrDict["TITLE"]
    self.theme = attrDict["THEME"]
    self.scale = 1
    self.showNumbers = attrDict["SHOW-NUMBERS"]
    self.editTitle = attrDict["EDIT-TITLE"]
    self.content = attrDict["CONTENT"]
    self.mainColor = attrDict["MainColor"]
    self.altColor1 = attrDict["AltColor1"]
    self.altColor2 = attrDict["AltColor2"]
    self.savePath = attrDict["SAVEPATH"]
    self.filename = attrDict["filename"]
    # other initializing vairables
    self.active = False
    self.menu = "CONTENT"  # can be "CONTENT" , "SETTINGS" , or "SAVE-PICKER"
    self.baseMargins = [5, 5]
    self.margins = self.baseMargins
    # cursor position setting
    if not cursorPos:
      self.cursorPos = len(self.content)
    else:
      self.cursorPos = cursorPos
    # icons
    self.icons = {
      "SAVE": None,
      "OPEN": None,
      "NEW": None,
      "SETTINGS": None
    }
    self.settingsIcons = {
      "THEME-YELLOW": None,
      "THEME-BLUE": None,
      "SHOW-NUMBERS": None
    }
    self.savedStickies = []
    self.loadIcons()
    print(self.icons)
    for i in self.icons:
      print(i)
    print(self.infoObj)
  
  def __str__(self):
    return ("Sticky of name: " + self.title + ", with a theme of: " + self.theme + ", with a content of length: " + str(len(self.content)) + ", Show Numbers: " + str(self.showNumbers))

  def checkMargins(self):
    if self.showNumbers:
      currLines = fcs.getTotalLines(self.content)+1  # +1 to account for the "starting at 0"
      digits = len(str(currLines))+1  # +1 for the extra sepparating line
      newMargins = [ self.baseMargins[0] + ( self.infoObj.textWriter.charDims[0] * digits ), self.baseMargins[1] ]
      self.margins = newMargins
    else:
      self.margins = self.baseMargins

  def loadIcons(self):
    self.icons = {
      "SAVE": icon("SAVE", (0, 0), ("ASSETS/SAVE-"+self.theme+".png"), (4, 4), self.iconSave, scale=self.scale),
      "NEW": icon("NEW", (0, 0), ("ASSETS/NEW-"+self.theme+".png"), (4, 4), self.iconNew, scale=self.scale),
      "OPEN": icon("OPEN", (0, 0), ("ASSETS/OPEN-"+self.theme+".png"), (4, 4), self.iconOpen, scale=self.scale),
      "SETTINGS": icon("SETTINGS", (0, 0), ("ASSETS/SETTINGS-"+self.theme+".png"), (4, 4), self.iconSettings, scale=self.scale),
      "ZOOM-PLUS": icon("ZOOM-PLUS", (0, 0), ("ASSETS/ZOOM-PLUS"+".png"), (4, 4), self.iconZoomPlus, scale=self.scale),
      "ZOOM-MINUS": icon("ZOOM-MINUS", (0, 0), ("ASSETS/ZOOM-MINUS"+".png"), (4, 4), self.iconZoomMinus, scale=self.scale)
    }
    # template: icon("NAME", (0, 0), ("ASSETS/NAME-"+self.theme+".png"), (4, 4), self.function)
    self.settingsIcons = {
      "THEME-YELLOW": clickableRect("YELLOW", (0, 0), (24, 24), (255, 218, 25), (25, 25, 25), (4, 4), self.iconChangeTheme, scale=self.scale),
      "THEME-ORANGE": clickableRect("ORANGE", (0, 0), (24, 24), (255, 114, 0), (25, 25, 25), (4, 4), self.iconChangeTheme, scale=self.scale),
      "THEME-PINK": clickableRect("PINK", (0, 0), (24, 24), (251, 93, 93), (25, 25, 25), (4, 4), self.iconChangeTheme, scale=self.scale),
      "THEME-PURPLE": clickableRect("PURPLE", (0, 0), (24, 24), (151, 53, 255), (25, 25, 25), (4, 4), self.iconChangeTheme, scale=self.scale),
      "THEME-BLUE": clickableRect("BLUE", (0, 0), (24, 24), (0, 164, 255), (25, 25, 25), (4, 4), self.iconChangeTheme, scale=self.scale),
      "THEME-GREEN": clickableRect("GREEN", (0, 0), (24, 24), (0, 163, 37), (25, 25, 25), (4, 4), self.iconChangeTheme, scale=self.scale),
      "SHOW-NUMBERS": toggleableImg("SHOW-NUMBERS-TOGGLE", (98, 34), (4, 4), ["ASSETS/UNCHECK.png", "ASSETS/CHECK.png"], self.iconShowNumbers, value=self.showNumbers),
      "EDIT-TITLE": toggleableImg("EDIT-TITLE-TOGGLE", (105, 67), (4, 4), ["ASSETS/UNCHECK.png", "ASSETS/CHECK.png"], self.iconEditTitle, value=self.editTitle)
    }
    # template: clickableRect("COLOUR", (x, 5), (24, 24), ("AltColor1"), (25, 25, 25), self.iconChangeTheme)

  def iconSave(self):
    sn = "TRUE" if self.showNumbers else "FALSE"
    et = "TRUE" if self.editTitle else "FALSE"
    # write
    toWrite = ("/TITLE " + self.title + "\n/THEME " + self.theme + "\n/SHOW-NUMBERS " + sn + "\n/EDIT-TITLE " + et + "\n/START-CONTENT\n" + self.content + "\n/END-CONTENT\n")
    f = open(self.savePath, "wt")
    f.write(toWrite)
    f.close()
    print("SAVED")
  
  def iconOpen(self):
    if self.menu == "OPEN":
      self.menu = "CONTENT"
    else:
      self.menu = "OPEN"
    self.savedStickies = []
    x, y = 0, 0
    for i in self.infoObj.stickies:
      self.savedStickies.append(stickySave((self.baseMargins[0]+x, self.baseMargins[1]+y), (self.infoObj.dispObj.res[0]-10, 15), self.baseMargins, i, self.infoObj.changeActive))
      y += 15 + self.baseMargins[1]

  def iconNew(self):
    print("classes.Sticky.iconNew called")
    fcs.makeNewSticky()
    self.infoObj.loadStickies()
    self.infoObj.changeActive("New Sticky")

  def iconSettings(self):
    if self.menu == "SETTINGS":
      self.menu = "CONTENT"
    else:
      self.menu = "SETTINGS"
  
  def scaleAllItems(self):
    # some information:
    # default icon res: 24x24
    # default icon res + margins: 32x32
    # default tooblar height: 32
    self.checkMargins()
    self.infoObj.dispObj.tbH = 32 * self.scale
    self.loadIcons()
    self.resetIconPositions()
    print("icon res:", self.icons["SAVE"].res)
    print("icon margins:", self.icons["SAVE"].margins)

  def iconZoomPlus(self):
    self.scale += 0.25
    self.infoObj.textWriter.scale(self.scale)
    print(self.infoObj.textWriter.pt)
    self.scaleAllItems()
  
  def iconZoomMinus(self):
    if self.scale > 1:
      self.scale -= 0.25
    self.infoObj.textWriter.scale(self.scale)
    self.scaleAllItems()
  
  def iconChangeTheme(self, color):
    if color in ["YELLOW", "ORANGE", "PINK", "PURPLE", "BLUE", "GREEN"]:
      self.theme = color
      self.iconSave()
    self.loadIcons()
    self.infoObj.loadStickies()
    self.infoObj.reset()
    print("new color: " + color)
  
  def iconShowNumbers(self, bool):
    self.showNumbers = bool
    self.checkMargins()
  
  def getAndSetTitle(self):
    contentSplit = self.content[:fcs.lenOfStringUntil(self.content, 0)].split(" ")
    # print(contentSplit)
    title = ""
    for word in contentSplit[1:]:
      title += word
      if word != contentSplit[-1]:
        title += " "
    self.title = title

  def iconEditTitle(self, bool):
    self.editTitle = bool
    print("New Edit Title value: " + str(self.editTitle))
    if self.editTitle and not self.content.startswith("TITLE: "):
      self.content = ("TITLE: " + self.title + "\n" + self.content)
    elif not self.editTitle and self.content.startswith("TITLE: "):
      # get and set title
      self.getAndSetTitle()
      # change content back
      self.content = self.content[fcs.lenOfStringUntil(self.content, 0)+1:]
      # save, change title
      self.iconSave()
      # rename file
      fcs.renameSticky(self.filename, self.title, self.infoObj)
      # reload
      self.infoObj.loadStickies()
      self.infoObj.changeActive(self.title)
  
  def drawToolbarIcons(self):
    for icon in self.icons:
      self.icons[icon].draw(self.infoObj.dispObj.surface)
  
  def drawSavePicker(self):
    for save in self.savedStickies:
      save.draw(self.infoObj.dispObj.surface, self.infoObj.textWriter)

  def drawSettings(self):
    # theme (item #1)
    self.infoObj.textWriter.write("Theme: ", (self.baseMargins[0], self.baseMargins[1]+(self.icons["SAVE"].res[1]/2-(self.infoObj.textWriter.charDims[1]/2))))
    # show numbers (item #2)
    self.infoObj.textWriter.write("Show Numbers: ", (self.baseMargins[0], self.baseMargins[1]+self.icons["SAVE"].res[1]+(self.icons["SAVE"].res[1]/2-(self.infoObj.textWriter.charDims[1]/2))))
    # edit title (item #3)
    self.infoObj.textWriter.write("Editing Title: ", (5, 80))
    # icons
    for icon in self.settingsIcons:
      self.settingsIcons[icon].draw(dispSurface=self.infoObj.dispObj.surface)
  
  def drawNumbers(self, drawSeparator=True):
    if self.showNumbers:
      lineStr = ""
      for i in range(fcs.getTotalLines(self.content)+1):
        lineStr += str(i+1)  + "\n"
      self.infoObj.textWriter.write(lineStr, self.baseMargins)
      if drawSeparator:
        pygame.draw.rect(self.infoObj.dispObj.surface, self.altColor1, (self.margins[0]-6, 0, 2, self.infoObj.dispObj.res[1]))
  
  def resetIconPositions(self):
    # TOOLBAR ICONS
    # get image res
    imgRes = self.icons["SAVE"].res
    margins = self.icons["SAVE"].margins
    x = margins[0]
    y = self.infoObj.dispObj.res[1]-self.infoObj.dispObj.tbH+margins[1]
    for icon in ICON_ORDER:
      self.icons[icon].move((x, y))
      x += imgRes[1]+2*(margins[0])
  
  def mouseDown(self):
    # toolbar icons
    for icon in self.icons:
      self.icons[icon].collide(pygame.mouse.get_pos(), autoCall=True)
    # settings icons if the settings menu is open
    if self.menu == "SETTINGS":
      for icon in self.settingsIcons:
        self.settingsIcons[icon].collide(pygame.mouse.get_pos(), autoCall=True)
    # save picker saves if the save picker menu is open
    elif self.menu == "OPEN":
      for save in self.savedStickies:
        save.collide(pygame.mouse.get_pos(), autoCall=True)
  
  def add(self, string):
    self.content = fcs.addCharAtPos(self.content, self.cursorPos, string)
    self.cursorPos += 1
    self.checkMargins()
  
  def backspace(self, amount=1):
    for _ in range(amount):
      if len(self.content) > 0 and self.cursorPos > 0:
        self.content = fcs.removeCharAtPos(self.content, self.cursorPos-1)
        self.cursorPos -= 1
    self.checkMargins()
  
  def directionHandle(self, direction):
    if direction == "LEFT":
      if self.cursorPos > 0:
        self.cursorPos -= 1
    if direction == "RIGHT":
      if self.cursorPos < len(self.content):
        self.cursorPos += 1
    if direction == "UP":
      # get current line
      currLine = fcs.getLineInString(self.content, self.cursorPos)
      if currLine == 0:
        self.cursorPos = 0
      else:
        # lengths
        lenOfLineUp = fcs.lenOfStringAtLine(self.content, currLine-1)
        lenOfLineNow = fcs.lenOfStringAtLine(self.content, currLine)
        # offsets
        negOffSetNow = ( fcs.lenOfStringUntil(self.content, currLine) - self.cursorPos )
        negOffSetAbove = ( negOffSetNow + (lenOfLineUp - lenOfLineNow) )
        posOffSetNow = ( fcs.lenOfStringAtLine(self.content, currLine) - (fcs.lenOfStringToIncluding(self.content, currLine) - self.cursorPos) )
        # if longer than where the cursor is
        if lenOfLineUp > posOffSetNow:
          self.cursorPos = ( fcs.lenOfStringUntil(self.content, currLine-1, offSetNegative=negOffSetAbove))
        # if shorter than where the cursor is
        else:
          self.cursorPos = ( fcs.lenOfStringToIncluding(self.content, currLine-1) )
    if direction == "DOWN":
      # get current line
      currLine = fcs.getLineInString(self.content, self.cursorPos)
      if currLine == fcs.getLineInString(self.content, len(self.content)):
        self.cursorPos = len(self.content)
      else:
        # lengths
        lenOfLineBelow = fcs.lenOfStringAtLine(self.content, currLine+1)
        lenOfLineNow = fcs.lenOfStringAtLine(self.content, currLine)
        # offsets
        negOffSetNow = ( fcs.lenOfStringUntil(self.content, currLine) - self.cursorPos )
        negOffSetBelow = ( negOffSetNow + (lenOfLineBelow - lenOfLineNow) )
        posOffSetNow = ( fcs.lenOfStringAtLine(self.content, currLine) - (fcs.lenOfStringToIncluding(self.content, currLine) - self.cursorPos) )
        # if longer than where the cursor is
        if lenOfLineBelow > posOffSetNow:
          self.cursorPos = ( fcs.lenOfStringUntil(self.content, currLine+1, offSetNegative=negOffSetBelow) )
        # if shorter than where the cursor is
        else:
          self.cursorPos = ( fcs.lenOfStringToIncluding(self.content, currLine+1) )

class graphicalContainer:
  def __init__(self, res, mainColor, altColor, toolbarHeight=32):
    self.res = res
    self.mainColor = mainColor
    self.altColor = altColor
    self.surface = pygame.display.set_mode(res, pygame.RESIZABLE)
    self.tbH = toolbarHeight  # tbH stands for toolbarHeight
  
  def drawBackground(self):
    pygame.draw.rect(self.surface, self.mainColor, (0, 0, self.res[0], self.res[1]))
  
  def drawToolbar(self):
    pygame.draw.rect(self.surface, self.altColor, (0, self.res[1]-self.tbH, self.res[0], self.tbH))

  def resize(self, newRes):
    self.surface = pygame.display.set_mode(newRes, pygame.RESIZABLE)
    self.res = newRes
