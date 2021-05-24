import pygame, pynput
import functions as fcs

class display:
  def __init__(self, name, mainCol, altCol, res=(150, 120)):
    self.name = name
    self.res = res
    self.surface = pygame.display.set_mode(res, pygame.RESIZABLE, pygame.NOFRAME)
    self.mainCol = mainCol
    self.altCol = altCol
    pygame.display.set_caption(self.name)
    self.focused = True
    self.tbH = 20
  
  def resize(self, newRes):
    self.surface = pygame.display.set_mode(newRes, pygame.RESIZABLE, pygame.NOFRAME)
    self.res = newRes
  
  def draw(self):
    # main area: (0, 0) -> (x, y-toolbarHeight)
    pygame.draw.rect(self.surface, self.mainCol, (0, 0, self.res[0], self.res[1]-self.tbH))
    pygame.draw.rect(self.surface, self.altCol, (0, self.res[1]-self.tbH, self.res[0], self.tbH))

DEF_FONT_INFO = [[5, 7, 2, 2], 1, "0123456789.ABCDEFGHIJKLMNOPQRSTUVWXYZ-,\"\'abcdefghijklmnopqrstuvwxyz`~!@#$%^&*()_[]{};:\\|<>/?=+"]
# items: [(wid, hi, horizMargin, vertiMargin), scale, [o, r, d, e, r, etc]

class clickableBox:
  def __init__(self, name, pos, res):
    self.name = name
    self.pos = pos
    self.res = res
  
  def __str__(self):
    return ("ClickableBox of name: \"" + self.name + "\", at pos: " + str(self.pos) + ", at res: " + str(self.size) + ".")
  
  def movePos(self, newPos):
    self.pos = newPos
  
  def collide(self, pos):
    if (self.pos[0] <= pos[0] <= self.pos[0]+self.res[0]) and (self.pos[1] <= pos[1] <= self.pos[1]+self.res[0]):
      return True
    return False
  
  def drawBorder(self, dispSurface, borderCol):
    pygame.draw.rect(dispSurface, borderCol, (self.pos[0], self.pos[1], self.res[0], 1))
    pygame.draw.rect(dispSurface, borderCol, (self.pos[0], self.pos[1], 1, self.pos[1]))
    pygame.draw.rect(dispSurface, borderCol, (self.pos[0], self.pos[1]+self.res[1], self.res[0], 1))
    pygame.draw.rect(dispSurface, borderCol, (self.pos[0]+self.res[0], self.pos[1], 1, self.res[1]))

class icon:
  def __init__(self, name, imgPath, pos):
    self.name = name
    self.img = pygame.image.load(imgPath)
    self.pos = pos
    self.res = (self.img.get_rect()[2], self.img.get_rect()[3])
  
  def __str__(self):
    return ("Icon of name: \"" + self.name + "\", at pos: " + str(self.pos) + ", at res: " + str(self.res) + ".")
  
  def movePos(self, newPos):
    self.pos = newPos
  
  def collide(self, pos):
    if (self.pos[0] <= pos[0] <= self.pos[0]+self.res[0]) and (self.pos[1] <= pos[1] <= self.pos[1]+self.res[0]):
      return True
    else:
      return False
  
  def draw(self, dispSurface):
    dispSurface.blit(self.img, self.pos)

ICON_ORDER = ["LOCK", "SAVE", "TRASH", "OPEN"]

class sticky:
  def __init__(self, displayObj, savePath, active, assetPath, fontImg, buttonHoverColor, margins=(5, 5), fontInfo=DEF_FONT_INFO):
    self.displayObj = displayObj
    self.displayObj.tbH = 30
    self.dispRes = displayObj.res
    self.title, self.theme, self.content = fcs.loadSticky(savePath)
    self.savePath = savePath
    self.assetPath = assetPath
    self.saved = True
    self.active = active
    self.fontImg = pygame.image.load(fontImg)
    self.fontImgOriRes = (self.fontImg.get_rect()[2], self.fontImg.get_rect()[3])
    self.fontInfo = fontInfo
    self.margins = margins
    self.bHC = buttonHoverColor
    # icons for actions
    self.icons = {}
    self.pickableSaves = {}
    # status variables
    self.locked = False
    self.deleteAttempts = 0  # for counting how many times it's pressed
    self.keyTracker = pynput.keyboard.Listener(on_press=self.kbrdPress, on_release=self.kbrdRelease)
    self.cursorPos = len(self.content)
    self.pressed = []
    self.arrows = {
      "UP": False,
      "DOWN": False,
      "LEFT": False,
      "RIGHT": False
    }
    self.special = {
      "SHIFT": False,
      "CTRL": False
    }
    # "init" function calling
    self.setIcons()
    self.setNewColors()
    self.moveIcons()
    self.autoResize()
    self.keyTracker.start()
    self.menu = 0  # 0 is sticky, 1 is save picker, 2 is settings
  
  def __str__(self):
    return ("Sticky of name: \"" + self.title + "\", saved: \"" + str(self.saved) + "\", active: \"" + str(self.active) + "\", content: \"" + self.content + "\"")
  
  def setIcons(self):
    self.icons = {
      "LOCKED": icon("LOCKED", self.assetPath+"LOCKED-"+self.theme+".png", (0, 0)),
      "UNLOCKED": icon("UNLOCKED", self.assetPath+"UNLOCKED-"+self.theme+".png", (0, 0)),
      "SAVE": icon("SAVE", self.assetPath+"SAVE-"+self.theme+".png", (0, 0)),
      "TRASH": icon("TRASH", self.assetPath+"TRASH-"+self.theme+".png", (0, 0)),
      "OPEN": icon("OPEN", self.assetPath+"OPEN-"+self.theme+".png", (0, 0))
    }
  
  def setNewColors(self):
    mC, aC1, aC2 = fcs.loadColors(self.theme, self.assetPath)
    self.hoverButtonColor = aC2
    self.displayObj.mainCol = mC
    self.displayObj.altCol = aC1
  
  def keyActions(self, key):
    try:
      # normal letters
      self.content = fcs.addCharAtPos(self.content, self.cursorPos, key.char)
      self.cursorPos += 1
    except:
      # space bar
      if key == pynput.keyboard.Key.space:
        self.content = fcs.addCharAtPos(self.content, self.cursorPos, " ")
        self.cursorPos += 1
      # enter key
      elif key == pynput.keyboard.Key.enter:
        self.content = fcs.addCharAtPos(self.content, self.cursorPos, "\n")
        self.cursorPos += 1
      # backspace
      elif key == pynput.keyboard.Key.backspace and self.cursorPos > 0:
        self.content = fcs.removeCharAtPos(self.content, self.cursorPos-1)
        self.cursorPos -= 1
      elif key == pynput.keyboard.Key.delete:
        try:
          self.content = fcs.removeCharAtPos(self.content, self.cursorPos)
        except IndexError:
          pass  # no action needed
    # arrows
    if self.arrows["LEFT"] and self.cursorPos > 0:
      self.cursorPos -= 1
      print(self.cursorPos)
    if self.arrows["RIGHT"] and self.cursorPos < len(self.content):
      self.cursorPos += 1
      print(self.cursorPos)
    if self.arrows["UP"] and self.cursorPos > 0:
      currLine = fcs.getLineInString(self.content, self.cursorPos)
      if currLine == 0:
        self.cursorPos = 0
      else:
        lenOfLineUp = fcs.lenOfStringAtLine(self.content, currLine-1)
        lenOfLineNow = fcs.lenOfStringAtLine(self.content, currLine)
        
        # offset information
        negOffSetNow = ( fcs.lenOfStringUntil(self.content, currLine) - self.cursorPos )
        negOffSetAbove = ( negOffSetNow + (lenOfLineUp - lenOfLineNow) )
        posOffSetNow = ( fcs.lenOfStringAtLine(self.content, currLine) - (fcs.lenOfStringToIncluding(self.content, currLine) - self.cursorPos) )
        print("nOSN: " + str(negOffSetNow))
        print("nOSA: " + str(negOffSetAbove))
        print("pOSN: " + str(posOffSetNow))
        
        # if longer than where the cursor is
        if lenOfLineUp > posOffSetNow:
          self.cursorPos = ( fcs.lenOfStringUntil(self.content, currLine-1, offSetNegative=negOffSetAbove))
        # if shorter than where the cursor is
        else:
          self.cursorPos = ( fcs.lenOfStringToIncluding(self.content, currLine-1) )
      print(self.cursorPos)
    if self.arrows["DOWN"] and self.cursorPos < len(self.content):
      currLine = fcs.getLineInString(self.content, self.cursorPos)
      if currLine == fcs.getLineInString(self.content, len(self.content)):
        self.cursorPos = len(self.content)
      else:
        lenOfLineBelow = fcs.lenOfStringAtLine(self.content, currLine+1)
        lenOfLineNow = fcs.lenOfStringAtLine(self.content, currLine)
        
        negOffSetNow = ( fcs.lenOfStringUntil(self.content, currLine) - self.cursorPos )
        negOffSetBelow = ( negOffSetNow + (lenOfLineBelow - lenOfLineNow) )
        posOffSetNow = ( fcs.lenOfStringAtLine(self.content, currLine) - (fcs.lenOfStringToIncluding(self.content, currLine) - self.cursorPos) )
        print("nOSN: " + str(negOffSetNow))
        print("nOSB: " + str(negOffSetBelow))
        print("pOSN: " + str(posOffSetNow))
        
        # if longer than where the cursor is
        if lenOfLineBelow > posOffSetNow:
          self.cursorPos = ( fcs.lenOfStringUntil(self.content, currLine+1, offSetNegative=negOffSetBelow) )
        # if shorter than where the cursor is
        else:
          self.cursorPos = ( fcs.lenOfStringToIncluding(self.content, currLine+1) )
        
      print(self.cursorPos)
  
  def kbrdPress(self, key):
    if not self.locked:
      try:
        if not key.char in self.pressed:
          self.pressed.append(key.char)
          # print(key)
      except:
        # print(key)
        if key == pynput.keyboard.Key.space:
          self.pressed.append(" ")
        # arrows
        elif key == pynput.keyboard.Key.up:
          self.arrows["UP"] = True
        elif key == pynput.keyboard.Key.down:
          self.arrows["DOWN"] = True
        elif key == pynput.keyboard.Key.left:
          self.arrows["LEFT"] = True
        elif key == pynput.keyboard.Key.right:
          self.arrows["RIGHT"] = True
        elif key == pynput.keyboard.Key.home:
          if self.special["CTRL"]:
            self.cursorPos = 0
          else:
            self.cursorPos = fcs.lenOfStringUntil(self.content, fcs.getLineInString(self.content, self.cursorPos)-1)+2
        elif key == pynput.keyboard.Key.end:
          if self.special["CTRL"]:
            self.cursorPos = len(self.content)
          else:
            self.cursorPos = fcs.lenOfStringToIncluding(self.content, fcs.getLineInString(self.content, self.cursorPos))
        elif key == pynput.keyboard.Key.shift or key == pynput.keyboard.Key.shift_r:
          self.special["SHIFT"] = True
        elif key == pynput.keyboard.Key.ctrl or key == pynput.keyboard.Key.ctrl_r:
          self.special["CTRL"] = True
        else:
          print(key)
      self.keyActions(key)
  
  def kbrdRelease(self, key):
    if not self.locked:
      try:
        if key.char in self.pressed:
          self.pressed.remove(key.char)
          # print(key.char)
      except:
        if key == pynput.keyboard.Key.space and " " in self.pressed:
          self.pressed.remove(" ")
        # arrows
        elif key == pynput.keyboard.Key.up:
          self.arrows["UP"] = False
        elif key == pynput.keyboard.Key.down:
          self.arrows["DOWN"] = False
        elif key == pynput.keyboard.Key.left:
          self.arrows["LEFT"] = False
        elif key == pynput.keyboard.Key.right:
          self.arrows["RIGHT"] = False
        elif key == pynput.keyboard.Key.shift or key == pynput.keyboard.Key.shift_r:
          self.special["SHIFT"] = False
        elif key == pynput.keyboard.Key.ctrl or key == pynput.keyboard.Key.ctrl_r:
          self.special["CTRL"] = False
          
  def moveIcons(self):
    iconLoc = 0
    for icon in ICON_ORDER:
      print(icon)
      # print(5+(24*(ICON_ORDER[1].find(self.icons[icon].name)/ICON_ORDER[0])))
      # self.icons[icon].movePos((5+(24*(ICON_ORDER[1].find(self.icons[icon].name)/ICON_ORDER[0])), self.displayObj.res[1]-27))
      if icon == "LOCK":
        self.icons["LOCKED"].movePos(((iconLoc*30)+3, self.displayObj.res[1]-self.displayObj.tbH+3))
        self.icons["UNLOCKED"].movePos(((iconLoc*30)+3, self.displayObj.res[1]-self.displayObj.tbH+3))
        print(self.icons["LOCKED"].pos)
      else:
        self.icons[icon].movePos(((iconLoc*30)+3, self.displayObj.res[1]-self.displayObj.tbH+3))
        print(self.icons[icon].pos)
      iconLoc += 1
  
  def autoResize(self, width=True, height=True):
    """
    # for me: (5, 7, 2, 2) / (wid, hi, margW, margH)
    # character
    print(fcs.findLongestLenBeforeNewline(self.content))
    print(fcs.findLinesInString(self.content))
    # character space taken up
    print(fcs.findLongestLenBeforeNewline(self.content)*self.fontInfo[0][0])
    print(fcs.findLinesInString(self.content)*self.fontInfo[0][1])
    # character space + margins between characters
    print(fcs.findLongestLenBeforeNewline(self.content)*self.fontInfo[0][0]+fcs.findLongestLenBeforeNewline(self.content)-1*self.fontInfo[0][2])
    print(fcs.findLinesInString(self.content)*self.fontInfo[0][1]+fcs.findLinesInString(self.content)-1*self.fontInfo[0][3])
    # chracter space + margins [all]
    print(fcs.findLongestLenBeforeNewline(self.content)*self.fontInfo[0][0]+fcs.findLongestLenBeforeNewline(self.content)-1*self.fontInfo[0][2]+(self.margins[0]*2))
    print(fcs.findLinesInString(self.content)*self.fontInfo[0][1]+fcs.findLinesInString(self.content)-1*self.fontInfo[0][3]+(self.margins[1]*2))
    """
    
    # actually setting res
    if width:
      self.displayObj.resize((fcs.findLongestLenBeforeNewline(self.content)*self.fontInfo[0][0]+fcs.findLongestLenBeforeNewline(self.content)-1*self.fontInfo[0][2]+(self.margins[0]*2), self.displayObj.res[1]))
    if height:
      self.displayObj.resize((self.displayObj.res[0], fcs.findLinesInString(self.content)*self.fontInfo[0][1]+fcs.findLinesInString(self.content)-1*self.fontInfo[0][3]+(self.margins[1]*2)))
  
  def setActive(self):
    self.active = True
  
  def setInactive(self):
    self.active = False
  
  def save(self):
    f = open(self.savePath, "w")
    # remove newline in content if neccessary
    self.content = fcs.rmNewline(self.content)
    # make and write info
    infoToWrite = ("/TITLE " + self.title + "\n/THEME " + self.theme + "\n/START-CONTENT\n" + self.content + "\n/END-CONTENT")
    f.write(infoToWrite)
    # finish up
    f.close()
    self.saved = True
  
  def delete(self):
    self.deleteAttemps += 1
    if self.deleteAttemps >= 2:
      fcs.removeFile(self.savePath)
  
  def eventCheck(self, event, debug=True):
    mPos = pygame.mouse.get_pos()
    if self.menu == 0:
      if event.type == pygame.MOUSEBUTTONDOWN:
        if self.icons["LOCKED"].collide(mPos) or self.icons["UNLOCKED"].collide(mPos):
          self.locked = fcs.flip(self.locked)
          if debug:
            print("Locked status: " + str(self.locked))
        elif self.icons["SAVE"].collide(mPos):
          self.save()
          if debug:
            print("Saved.")
        elif self.icons["TRASH"].collide(mPos):
          self.delete()
          if debug:
            print("Trash clicked. Attempts at: " + str(self.deleteAttempts))
    elif self.menu == 1:
      pass
  
  def draw(self, dispSurface, content=True, icons=True, debug=False):
    # some 'maintenance' first
    if self.displayObj.res != self.dispRes:
      self.dispRes = self.displayObj.res
      self.moveIcons()
    # now for the actual drawing
    if content:
      if self.menu == 0:  # normal menu
        x = self.margins[0]
        y = self.margins[1]
        contentLoc = 0
        cursorDrawn = False
        if debug:
          print("Starting Drawing Content")
        for char in self.content:
          if contentLoc == self.cursorPos:
            pygame.draw.rect(dispSurface, (25, 25, 25), (x, y, self.fontInfo[0][0], self.fontInfo[0][1]))
            x += self.fontInfo[0][0]+self.fontInfo[0][2]
            cursorDrawn = True
          elif char == " ":
            x += self.fontInfo[0][0]+self.fontInfo[0][2]
          else:
            # for non-space characters
            dispSurface.blit(self.fontImg, (x, y), area=((self.fontInfo[2].find(char)*self.fontInfo[0][0]), 0, self.fontInfo[0][0], self.fontInfo[0][1]))
            if debug:
              print(self.fontImg, (x, y), ((self.fontInfo[2].find(char)*self.fontInfo[0][0]), 0, self.fontInfo[0][0], self.fontInfo[0][1]))
            x += self.fontInfo[0][0]+self.fontInfo[0][2]
          if char == "\n":
            x = self.margins[0]
            y += self.fontInfo[0][1]+self.fontInfo[0][3]
          contentLoc += 1
        if not cursorDrawn:
          pygame.draw.rect(dispSurface, (25, 25, 25), (x, y, self.fontInfo[0][0], self.fontInfo[0][1]))
        if debug:
          print("Done Drawing Content")
      elif self.menu == 1:  # save picker
        x = self.margins[0]
        y = self.margins[1]
        for sticky in self.pickableSaves:
          for char in sticky:
            if char == " ":  # spaces
              x += self.fontInfo[0][0]+self.fontInfo[0][2]
            else:  # normal characters
              dispSurface.blit(self.fontImg, (x, y), area=((self.fontInfo[2].find(char)*self.fontInfo[0][0]), 0, self.fontInfo[0][0], self.fontInfo[0][1]))
          
      elif self.menu == 2:  # settings menu
        pass
    if icons:
      # icon drawing
      for icon in self.icons:
        if icon != "LOCKED" and icon != "UNLOCKED":
          dispSurface.blit(self.icons[icon].img, self.icons[icon].pos)
        if self.icons[icon].collide(pygame.mouse.get_pos()):
          # draw a very inefficent rectangle.
          pygame.draw.rect(dispSurface, self.bHC, (self.icons[icon].pos[0]-3, self.icons[icon].pos[1]-3, 30, 1))  # top-left -> right
          pygame.draw.rect(dispSurface, self.bHC, (self.icons[icon].pos[0]-3, self.icons[icon].pos[1]-3, 1, 30))  # top-left -> down
          pygame.draw.rect(dispSurface, self.bHC, (self.icons[icon].pos[0]-3, self.icons[icon].pos[1]+2+self.icons[icon].res[1], 30, 1))  # bottom-left -> right
          pygame.draw.rect(dispSurface, self.bHC, (self.icons[icon].pos[0]+2+self.icons[icon].res[0], self.icons[icon].pos[1]-3, 1, 30))  # top-right -> down
      if self.locked:
        dispSurface.blit(self.icons["LOCKED"].img, self.icons["LOCKED"].pos)
      else:
        dispSurface.blit(self.icons["UNLOCKED"].img, self.icons["UNLOCKED"].pos)
