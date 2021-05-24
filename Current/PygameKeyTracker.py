import pygame

keyDictList = [13, 32, 39, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 61, 91, 92, 93, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]
keyArrowsList = [1073741904, 1073741903, 1073741906, 1073741905]
keyDictLowercase = {
   "8": "BKSP", "13": "\n", "32": " ","39": "'","44": ",","45": "-","46": ".","47": "/","48": "0","49": "1","50": "2","51": "3","52": "4","53": "5","54": "6","55": "7","56": "8","57": "9","59": ";","61": "=","91": "[","92": "\\","93": "]","96": "`","97": "a","98": "b","99": "c","100": "d","101": "e","102": "f","103": "g","104": "h","105": "i","106": "j","107": "k","108": "l","109": "m","110": "n","111": "o","112": "p","113": "q","114": "r","115": "s","116": "t","117": "u","118": "v","119": "w","120": "x","121": "y","122": "z", "1073741904": "LEFT", "1073741903": "RIGHT", "1073741906": "UP", "1073741905": "DOWN"
}
keyDictUppercase = {
  "8": "BKSP", "13": "\n", "32": " ","39": "\"","44": "<","45": "_","46": ">","47": "?","48": ")","49": "!","50": "@","51": "#","52": "$","53": "%","54": "^","55": "&","56": "*","57": "(","59": ":","61": "+","91": "{","92": "|","93": "}","96": "~","97": "A","98": "B","99": "C","100": "D","101": "E","102": "F","103": "G","104": "H","105": "I","106": "J","107": "K","108": "L","109": "M","110": "N","111": "O","112": "P","113": "Q","114": "R","115": "S","116": "T","117": "U","118": "V","119": "W","120": "X","121": "Y","122": "Z", "1073741904": "LEFT", "1073741903": "RIGHT", "1073741906": "UP", "1073741905": "DOWN"
}
keySpecials = {
  "LSHIFT": "1073742049","RSHIFT": "1073742053","LCTRL": "1073742048","RCTRL": "1073742052"
}

class KeyTracker:
  def __init__(self, addFunc, popFunc, directionFunc, insertAuto=True, repeatDelay=0.5, fps=30):
    self.addF = addFunc
    self.popF = popFunc
    self.directionF = directionFunc
    self.pressed = []
    self.repeatingChar = None
    self.specialPressed = []
    self.repeatCounter = 0
    self.fps = 30
    self.repeatLimit = fps*repeatDelay
    self.repeatDelay = repeatDelay
    self.insertAuto = insertAuto
    self.specialPressed = {
      "SHIFT": False, 
      "CTRL": False
    }
  
  def elimAllNotPressed(self, keys):
    for i in self.pressed:
      if not keys[i]:
        self.pressed.remove(i)

  def addToText(self, keyCode):
    if self.specialPressed["SHIFT"]:
      self.addF(keyDictUppercase[str(keyCode)])
    else:
      self.addF(keyDictLowercase[str(keyCode)])

  def repeater(self):
    try:
      if len(self.pressed) == 0:
        self.repeatingChar = None
        self.repeatCounter = 0
      
      if (len(self.pressed) > 0) and not self.repeatingChar:
        self.repeatingChar = self.pressed[-1]
        self.repeatCounter = 0
      elif self.repeatingChar != self.pressed[-1]:
        self.repeatingChar = self.pressed[-1]
        self.repeatCounter = 0
      elif self.repeatingChar and self.repeatCounter <= self.repeatLimit:
        self.repeatCounter += 1
      else:
        if self.repeatingChar == 8:
          self.popF()
        elif (1073741903 <= self.repeatingChar <= 1073741906):
          self.directionF(keyDictLowercase[str(self.repeatingChar)])
        else:
          self.addToText(self.repeatingChar)
    except IndexError:
      pass

  def checkKeys(self):
    keys = pygame.key.get_pressed()
      
    # modifiers
    if keys[1073742049] or keys[1073742053]:
      self.specialPressed["SHIFT"] = True
    else:
      self.specialPressed["SHIFT"] = False
    if keys[1073742048] or keys[1073742052]:
      self.specialPressed["CTRL"] = True
    else:
      self.specialPressed["CTRL"] = False

    # backspace
    if keys[8] and not (8 in self.pressed):
      self.pressed.append(8)
      self.popF()

    # arrows
    for i in keyArrowsList:
      if keys[i] and not (i in self.pressed):
        self.pressed.append(i)
        self.directionF(keyDictLowercase[str(i)])

    for i in keyDictList:
      if keys[i] and not (i in self.pressed):
        self.pressed.append(i)
        self.addToText(i)
    
    self.elimAllNotPressed(keys)
    self.repeater()