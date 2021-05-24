import pygame

pygameKeys = {
  # numpad
  256: "0",
  257: "1",
  258: "2",
  259: "3",
  260: "4",
  261: "5",
  262: "6",
  263: "7",
  264: "8",
  265: "9",
  267: "/",
  268: "*",
  269: "-",
  270: "+",
  # number row + symbols
  49: ["1", "!"],
  50: ["2", "@"],
  51: ["3", "#"],
  52: ["4", "$"],
  53: ["5", "%"],
  54: ["6", "^"],
  55: ["7", "&"],
  56: ["8", "*"],
  57: ["9", "("],
  48: ["0", ")"],
  # other symbols
  96: ["`", "~"],
  45: ["-", "_"],
  61: ["=", "+"],
  91: ["[", "{"],
  93: ["]", "}"],
  92: ["\\", "|"],
  59: [";", ":"],
  39: ["'", "\""],
  44: [",", "<"],
  46: [".", ">"],
  47: ["/", "?"],
  # actual letters
  97: ["a", "A"],
  98: ["b", "B"],
  99: ["c", "C"],
  100: ["d", "D"],
  101: ["e", "E"],
  102: ["f", "F"],
  103: ["g", "G"],
  104: ["h", "H"],
  105: ["i", "I"],
  106: ["j", "J"],
  107: ["k", "K"],
  108: ["l", "L"],
  109: ["m", "M"],
  110: ["n", "N"],
  111: ["o", "O"],
  112: ["p", "P"],
  113: ["q", "Q"],
  114: ["r", "R"],
  115: ["s", "S"],
  116: ["t", "T"],
  117: ["u", "U"],
  118: ["v", "V"],
  119: ["w", "W"],
  120: ["x", "X"],
  121: ["y", "Y"],
  122: ["z", "Z"],
  32: [" ", " "]
}

class tracker:
  def __init__(self, mode):
    # mode can be one of the following: "pygame" or "pynput"
    self.pressed = []
    self.latest = None
    self.mods = {
      "SHIFT": False,
      "CTRL": False,
      "ALT": False,
      "RETURN": False,
      "BACKSPACE": False,
      "DELETE": False
    }
    self.arrows = {
      "UP": False,
      "DOWN": False,
      "LEFT": False,
      "RIGHT": False
    }
    self.mode = mode
  
  def modPressed(self, which="0"):
    # which can be 0 for all, 1 for SHIFT/CTRL/ALT, 2 for RETURN/BACKSPACE/DELETE
    i = False
    for mod in self.mods:
      if ("0" in which or "1" in which) and (mod == "SHIFT" or mod == "CTRL" or mod == "ALT"):
        if self.mods[mod]:
          i = True
      if ("0" in which or "2" in which) and (mod == "RETURN" or mod == "BACKSPACE" or mod == "DELETE"):
        if self.mods[mod]:
          i = True
    return i
  
  def keyPressed(self, key):
    if self.mode == "pygame":
      # mods first
      if key == 303 or key == 304:
        self.mods["SHIFT"] = True
      elif key == 305 or key == 306:
        self.mods["CTRL"] = True
      elif key == 307 or key == 308:
        self.mods["ALT"] = True
      elif key == 13 or key == 271:
        self.mods["RETURN"] = True
      elif key == 8:
        self.mods["BACKSPACE"] = True
      elif key == 127 or key == 266:
        self.mods["DELETE"] = True
      # arrow keys
      elif key == 273:
        self.arrows["UP"] = True
      elif key == 274:
        self.arrows["DOWN"] = True
      elif key == 275:
        self.arrows["RIGHT"] = True
      elif key == 276:
        self.arrows["LEFT"] = True
      # then, normal keys
      else:
        if key in pygameKeys:
          if self.mods["SHIFT"]:
            # if shift is pressed down
            self.pressed.append(pygameKeys[key][1])
            self.latest = pygameKeys[key][1]
          else:
            # shift it not pressed down
            self.pressed.append(pygameKeys[key][0])
            self.latest = pygameKeys[key][0]
        else:
          self.latest = None
  
  def keyReleased(self, key):
    if self.mode == "pygame":
      # mods first
      if key == 303 or key == 304:
        self.mods["SHIFT"] = False
      elif key == 305 or key == 306:
        self.mods["CTRL"] = False
      elif key == 307 or key == 308:
        self.mods["ALT"] = False
      elif key == 13 or key == 271:
        self.mods["RETURN"] = False
      elif key == 8:
        self.mods["BACKSPACE"] = False
      elif key == 127 or key == 266:
        self.mods["DELETE"] = False
      # arrow keys
      elif key == 273:
        self.arrows["UP"] = False
      elif key == 274:
        self.arrows["DOWN"] = False
      elif key == 275:
        self.arrows["RIGHT"] = False
      elif key == 276:
        self.arrows["LEFT"] = False
      # then, normal keys
      else:
        if key in pygameKeys:
          try:
            self.pressed.remove(pygameKeys[key][0])
          except ValueError:
            self.pressed.remove(pygameKeys[key][1])
        if len(self.pressed) < 1:
          self.latest = None

