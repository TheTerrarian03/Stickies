import os

### small functions
def returnOnlyActive(stickyObjList, defaultIndex=0):
  for sticky in stickyObjList:
    if sticky.active:
      return sticky
      
  if not found:
    return stickyObjList[defaultIndex]

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

def getSavesList(savesFolder):
  # empty list
  lst = []
  
  # parse files, and add only if they're a save file
  for File in os.listdir(savesFolder):
    if File.endswith(".sticky"):
      lst.append(File)
  
  # return list
  return lst

def flip(boolVal):
  if boolVal:
    return False
  else:
    return True

def removeFile(filePath):
  os.remove(filePath)

def rmNewline(string):
  if string.endswith("\n"):
    return string[:-1]
  return string

def replaceCharAtPos(string, position, newChar):
  # convert to list
  lst = []
  for char in string:
    lst.append(char)
  # replace
  lst[position] = newChar
  # convert to string
  newString = ""
  for char in lst:
    newString += char
  return newString

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

def addCharAtPos(string, position, whatToAdd):
  #  convert to list
  lst = []
  for char in string:
    lst.append(char)
  # add
  lst.insert(position, whatToAdd)
  # convert to string
  newString = ""
  for char in lst:
    newString += char
  return newString

def findLongestLenBeforeNewline(string):
  longestLen = 0
  currLen = 0
  for char in string:
    if char != "\n":
      currLen += 1
    else:
      if currLen > longestLen:
        longestLen = currLen
      currLen = 0
  return longestLen

def findLinesInString(string, splitChar="\n"):
  return len(string.split(splitChar))

def stringToIntList(string, separator):
  sSplit = string.split(separator)
  lst = []
  for i in sSplit:
    lst.append(int(i))
  
  return lst

### larger functions
def loadColors(targetColor, assetPath):
  f = open(assetPath+"COLORS.txt")
  
  found = False
  mainCol = None
  altCol1 = None
  altCol2 = None
  
  for line in f:
    lineS = line.split(" ")
    if lineS[0] == targetColor:
      found = True
      mainCol = stringToIntList(lineS[1], "-")
      altCol1 = stringToIntList(lineS[2], "-")
      altCol2 = stringToIntList(lineS[3], "-")
  
  return mainCol, altCol1, altCol2

def loadSettings(filename):
  f = open(filename, "rt")
  
  # initialize variables
  saveloc, mainCol, altCol1, altCol2, defTitle, font, fps, assetsFolder = (None, None, None, None, None, None, None, None)
  
  # parsing information
  for line in f:
    lineS = line.split(" ")
    if lineS[0] == "SAVES":
      saveLoc = lineS[1]
    elif lineS[0] == "MAIN_COL":
      mainCol = []
      for rgbVal in lineS[1].split("-"):
        mainCol.append(int(rgbVal))
    elif lineS[0] == "ALT_COL_1":
      altCol1 = []
      for rgbVal in lineS[1].split("-"):
        altCol1.append(int(rgbVal))
    elif lineS[0] == "ALT_COL_2":
      altCol2 = []
      for rgbVal in lineS[1].split("-"):
        altCol2.append(int(rgbVal))
    elif lineS[0] == "DEF_TITLE":
      defTitle = lineS[1]
    elif lineS[0] == "FONT":
      font = lineS[1]
    elif lineS[0] == "FPS":
      fps = int(lineS[1])
    elif lineS[0] == "ASSETS":
      assetsFolder = lineS[1]
  
  # removing newlines if needed
  if saveLoc.endswith("\n"):
    saveLoc = saveLoc[:-1]
  if defTitle.endswith("\n"):
    defTitle = defTitle[:-1]
  if font.endswith("\n"):
    font = font[:-1]
  if assetsFolder.endswith("\n"):
    assetsFolder = assetsFolder[:-1]
  
  return (saveLoc, mainCol, altCol1, altCol2, defTitle, font, fps, assetsFolder)

def loadSticky(path):
  f = open(path, "rt")
  
  # initialize variables
  title = None
  theme = None
  fontScale = 0
  mainColor, secondColor, textNormal, textHighlight = (None, None, None, None)
  content = ""
  contentStarted = False  # not returned
  contentDone = False  # also not returned
  
  # parse information
  for line in f:
    if line.split(" ")[0] == "/TITLE":
      title = line.split(" ")[1]
    elif line.startswith("/THEME"):
      theme = line.split(" ")[1]
    elif line.startswith("/START-CONTENT"):
      contentStarted = True
    elif line.startswith("/END-CONTENT"):
      contentStarted = False
      contentDone = True
    else:
      if contentStarted and not contentDone:
        content += line
  
  # remove newlines if necessary
  if title.endswith("\n"):
    title = title[:-1]
  if theme.endswith("\n"):
    theme = theme[:-1]
  if content.endswith("\n"):
    content = content[:-1]
  
  print(title, theme, content)
  
  return title, theme, content

