import pygame
import functions as fcs

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
  def __init__(self, name, pos, res, mainColor, borderColor, function):
    self.name = name
    self.pos = pos
    self.res = res
    self.mC = mainColor
    self.bC = borderColor
    self.func = function
  
  def collide(self, mPos, autoCall=False):
    if (self.pos[0] <= mPos[0] <= self.pos[0]+self.res[0]) and (self.pos[1] <= mPos[1] <= self.pos[1]+self.res[1]):
      if autoCall:
        self.func(self.name)
      else:
        return True
    return False
  
  def draw(self, dispSurface):
    pygame.draw.rect(dispSurface, self.bC, (self.pos[0], self.pos[1], self.res[0], self.res[1]))  # border
    pygame.draw.rect(dispSurface, self.mC, (self.pos[0]+2, self.pos[1]+2, self.res[0]-4, self.res[1]-4))  # inside

class icon:
  def __init__(self, name, pos, iconPath, margins, function):
    self.name = name
    self.img = pygame.image.load(iconPath)
    self.margins = margins
    self.func = function
    self.pos = pos
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

ICON_ORDER = ["SAVE", "OPEN", "NEW", "SETTINGS"]

class Sticky:
  def __init__(self, reloadFunction, getStickiesFunction, changeActiveFunction, displayObj, attrDict, cursorPos=None):
    # functions from main file
    self.reloadFunc = reloadFunction
    self.getStickies = getStickiesFunction
    self.changeActive = changeActiveFunction
    self.dispObj = displayObj
    # set info from attrDict
    self.title = attrDict["TITLE"]
    self.theme = attrDict["THEME"]
    self.showNumbers = attrDict["SHOW-NUMBERS"]
    self.content = attrDict["CONTENT"]
    self.mainColor = attrDict["MainColor"]
    self.altColor1 = attrDict["AltColor1"]
    self.altColor2 = attrDict["AltColor2"]
    self.savePath = attrDict["SAVEPATH"]
    # other initializing vairables
    self.active = False
    self.menu = "CONTENT"  # can be "CONTENT" , "SETTINGS" , or "SAVE-PICKER"
    self.baseMargins = [5, 5]
    self.margins = self.baseMargins
    self.editingTitle = False
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
    self.checkMargins()
  
  def __str__(self):
    return ("Sticky of name: " + self.title + ", with a theme of: " + self.theme + ", with a content of length: " + str(len(self.content)) + ", Show Numbers: " + str(self.showNumbers))

  def checkMargins(self):
    if self.showNumbers:
      currLines = fcs.getTotalLines(self.content)+1  # +1 to account for the "starting at 0"
      digits = len(str(currLines))+1  # +1 for the extra sepparating line
      newMargins = [ self.baseMargins[0] + ( 7 * digits ), self.baseMargins[1] ]
      self.margins = newMargins
    else:
      self.margins = self.baseMargins

  def loadIcons(self):
    self.icons = {
      "SAVE": icon("SAVE", (0, 0), ("ASSETS/SAVE-"+self.theme+".png"), (4, 4), self.iconSave),
      "NEW": icon("NEW", (0, 0), ("ASSETS/NEW-"+self.theme+".png"), (4, 4), self.iconNew),
      "OPEN": icon("OPEN", (0, 0), ("ASSETS/OPEN-"+self.theme+".png"), (4, 4), self.iconOpen),
      "SETTINGS": icon("SETTINGS", (0, 0), ("ASSETS/SETTINGS-"+self.theme+".png"), (4, 4), self.iconSettings)
    }
    self.settingsIcons = {
      "THEME-YELLOW": clickableRect("YELLOW", (53, 5), (24, 24), (255, 218, 25), (25, 25, 25), self.iconChangeTheme),
      "THEME-BLUE": clickableRect("BLUE", (89, 5), (24, 24), (0, 164, 255), (25, 25, 25), self.iconChangeTheme),
      "SHOW-NUMBERS": toggleableImg("SHOW-NUMBERS-TOGGLE", (98, 34), (4, 4), ["ASSETS/UNCHECK.png", "ASSETS/CHECK.png"], self.iconShowNumbers, value=self.showNumbers)
    }

  def iconSave(self):
    sn = "TRUE" if self.showNumbers else "FALSE"
    toWrite = ("/TITLE " + self.title + "\n/THEME " + self.theme + "\n/SHOW-NUMBERS " + sn + "\n/START-CONTENT\n" + self.content + "\n/END-CONTENT\n")
    f = open(self.savePath, "wt")
    f.write(toWrite)
    f.close()
    print("SAVED")
  
  def iconOpen(self):
    # print("classes.Sticky.iconOpen called")
    if self.menu == "OPEN":
      self.menu = "CONTENT"
    else:
      self.menu = "OPEN"
    self.savedStickies = []
    x, y = 0, 0
    for i in self.getStickies():
      self.savedStickies.append(stickySave((self.baseMargins[0]+x, self.baseMargins[1]+y), ((8+len(i.title)*7), 15), self.baseMargins, i, self.changeActive))
      y += 15 + self.baseMargins[1]

  def iconNew(self):
    print("classes.Sticky.iconNew called")
    fcs.makeNewSticky()

  def iconSettings(self):
    # print("classes.Sticky.iconSettings called")
    if self.menu == "SETTINGS":
      self.menu = "CONTENT"
    else:
      self.menu = "SETTINGS"
  
  def iconChangeTheme(self, color):
    if color in ["YELLOW", "BLUE"]:
      self.theme = color
      self.iconSave()
    self.loadIcons()
    self.reloadFunc()
    print("new color: " + color)
  
  def iconShowNumbers(self, bool):
    self.showNumbers = bool
    self.checkMargins()
  
  def drawToolbarIcons(self, dispSurface):
    for icon in self.icons:
      self.icons[icon].draw(dispSurface)
  
  def drawSavePicker(self, dispSurface, pTW):
    for save in self.savedStickies:
      save.draw(dispSurface, pTW)

  def drawSettings(self, dispSurface, pTW):
    # theme (item #1)
    pTW.write("Theme: ", (5, 14))
    # show numbers (item #2)
    pTW.write("Show Numbers: ", (5, 47))
    # icons
    for icon in self.settingsIcons:
      self.settingsIcons[icon].draw(dispSurface=dispSurface)
  
  def drawNumbers(self, pTW, drawSeparator=True):
    if self.showNumbers:
      lineStr = ""
      for i in range(fcs.getTotalLines(self.content)+1):
        lineStr += str(i+1)  + "\n"
      pTW.write(lineStr, self.baseMargins)
      if drawSeparator:
        pygame.draw.rect(self.dispObj.surface, self.altColor1, (self.margins[0]-6, 0, 2, self.dispObj.res[1]))
  
  def resetIconPositions(self, dispRes):
    x = 4
    y = dispRes[1]-28
    for icon in ICON_ORDER:
      if icon == "LOCK":
        pass
      else:
        self.icons[icon].move((x, y))
        x += 32
  
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
