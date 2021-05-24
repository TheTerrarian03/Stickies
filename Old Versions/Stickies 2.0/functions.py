import os

### small functions
def flip(bool):
  if bool:
    return False
  return True

def stringToIntList(string, seperator):
  stringS = string.split(seperator)
  lst = []
  for i in stringS:
    lst.append(int(i))
  return lst

def returnOnlyActive(objList):
  for obj in objList:
    if obj.active:
      return obj

def rOA(objList):
  return returnOnlyActive(objList)

def removeCharAtPos(string, position):
  if len(string) > 0:
    # convert to list
    lst = []
    for char in string:
      lst.append(char)
    # delete
    lst.pop(position)
    # convert to string
    newString = ""
    for char in lst:
      newString += char
    return newString

def addCharAtPos(string, position, toAdd):
  #  convert to list
  lst = []
  for char in string:
    lst.append(char)
  # add
  lst.insert(position, toAdd)
  # convert to string
  newString = ""
  for char in lst:
    newString += char
  return newString

def getTotalLines(string, newline="\n"):
  lines = 0
  for i in string:
    if i == newline:
      lines += 1
  return lines

# below code is copied and pasted, so if something goes wrong blame the CMD+C and CMD+V

def getLineInString(string, atPos, start=0):
  currLine = start
  for char in range(atPos):
    if string[char] == "\n":
      currLine += 1
  # print(currLine)
  return currLine

def lenOfStringAtLine(string, lineNum):
  return len(string.split("\n")[lineNum])

def lenOfStringUntil(string, line, offSetNegative=0):
  ### this function will return how many characters UNTIL (not including) the line you provide
    # this INCLUDES the newline character.
  # offSetNegative means how much to add, from the end of the line
  currLine = 0
  currLen = 0
  # beginning parsing
  for i in range(len(string)):
    if string[i] == "\n":
      currLine += 1
    if currLine == line:
      break
    currLen += 1
  # extra / offset
  extra = ( len(string.split("\n")[line]) - offSetNegative )
  return currLen + extra

def lenOfStringToIncluding(string, line, offSetNegative=0):
  ### this function will return how many characters until THE END OF THE LINE that you provide
    # this INCLUDES the newline character
  # offSetNegative means how to subtract, from the end of the line
  currLine = 0
  currLen = 0
  # begin parsing
  for i in range(len(string)):
    if string[i] == "\n":
      currLine += 1
    if currLine > line:
      break
    currLen += 1
  return currLen - offSetNegative

### bigger functions
def makeNewSticky():
  print("Adding new files is not implemented yet.")

def loadStickies():
  stickyList = []
  
  print(os.listdir("SAVES/"))
  for File in os.listdir("SAVES/"):
    if File.endswith(".sticky"):
      stickyAttr = {"TITLE": None, "THEME": None, "SHOW-NUMBERS": None, "CONTENT": "", "MainColor": [], "AltColor1": [], "AltColor2": [], "SAVEPATH": None}
      ctSt = False
      done = False
      f = open("SAVES/"+File)
      # going through the lines, for title, theme, and content
      for line in f:
        lineS = line.split(" ")
        if lineS[0] == "/TITLE":
          stickyAttr["TITLE"] = lineS[1]
        elif lineS[0] == "/THEME":
          stickyAttr["THEME"] = lineS[1]
        elif lineS[0] == "/SHOW-NUMBERS":
          if lineS[1] == "TRUE\n":
            stickyAttr["SHOW-NUMBERS"] = True
          elif lineS[1] == "FALSE\n":
            stickyAttr["SHOW-NUMBERS"] = False
        elif lineS[0] == "/START-CONTENT\n":
          ctSt = True
        elif lineS[0] == "/END-CONTENT\n":
          ctSt = False
          done = True
        else:
          if ctSt and not done:
            stickyAttr["CONTENT"] += line
      # remove newlines if necessary
      if stickyAttr["TITLE"].endswith("\n"):
        stickyAttr["TITLE"] = stickyAttr["TITLE"][:-1]
      if stickyAttr["THEME"].endswith("\n"):
        stickyAttr["THEME"] = stickyAttr["THEME"][:-1]
      if stickyAttr["CONTENT"].endswith("\n"):
        stickyAttr["CONTENT"] = stickyAttr["CONTENT"][:-1]
      # adding colors to the stickyAttr 's
      f.close()
      f = open("COLORS.txt", "rt")
      for line in f:
        lineS = line.split(" ")
        if lineS[0] == stickyAttr["THEME"]:
          stickyAttr["MainColor"] = stringToIntList(lineS[1], "-")
          stickyAttr["AltColor1"] = stringToIntList(lineS[2], "-")
          stickyAttr["AltColor2"] = stringToIntList(lineS[3], "-")
      stickyAttr["SAVEPATH"] = "SAVES/"+File
      stickyList.append(stickyAttr)
  return stickyList
