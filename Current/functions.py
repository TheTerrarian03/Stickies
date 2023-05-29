import classes, os, sys, json

def getOS():
    osName = sys.platform
    if osName == "linux":
        return "linux"
    elif osName == "darwin":
        return "macOS"
    elif osName == "windows":
        return "windows"

def toUpperAndLowerAlternating(string):
    new = ""
    for i in range(len(string)):
        if i % 2 == 0:
            new += string[i].upper()
        else:
            new += string[i].lower()
    return new

def returnOnlyActive(objList):
    for obj in objList:
        if obj.active:
            return obj

def rOA(objList):
  return returnOnlyActive(objList)

def deleteFile(filePath):
    os.remove(filePath)

def setLastOpen(title):
    f = open("SETTINGS.txt", "wt")
    f.write("/LAST-OPEN "+title + "\n")
    f.close()

def getLastOpen():
    f = open("SETTINGS.txt", "rt")

    for line in f:
        lineS = line.split(" ")
        if lineS[0] == "/LAST-OPEN":
            f.close()
            return lineS[1][:-1]

def makeColorDict(theme):
    # open file to read ("COLORS.txt" is the default)
    f = open("COLORS.txt", "rt")
    # find and set info
    colorDict = {"main": None, "alt1": None, "alt2": None, "text": None}
    for line in f:
        lineS = line.split(" ")
        if lineS[0] == theme:
            colorDict["main"] = lineS[1]
            colorDict["alt1"] = lineS[2]
            colorDict["alt2"] = lineS[3]
            colorDict["text"] = lineS[4][:-1]
    # close file and return
    f.close()
    return colorDict

def setNewActive(objList, newActivesTitle):
    for obj in objList:
        obj.active = False
    
    for obj in objList:
        if obj.title == newActivesTitle:
            obj.active = True
    
    return objList

def returnObjWithSamePath(objList, filePath):
    for obj in objList:
        if obj.filePath == filePath:
            return obj

def makeNewSticky(returnTitle=False, makeSave=True):
    # makeSave changes whether this function actually makes the file.
    currName = "NewSticky"
    addNum = 1
    looping = True

    while looping:
        if not os.path.exists("SAVES/"+currName+str(addNum)+".sticky"):
            if makeSave:
                toWriteData = {"TITLE": (currName + str(addNum)), "THEME": "YELLOW", "CONTENT": "Welcome to your new sticky!\nComplain about life here! Or make a to do list.\nOr, do whatever!\n\nEnjoy.\n-Logan Meyers :)\n"}
                toWriteJson = json.dumps(toWriteData)
                f = open("SAVES/"+currName+str(addNum)+".sticky", "wt")
                f.write(toWriteJson)
                f.close()
                looping = False
            else:
                looping = False
        else:
            addNum += 1
    
    if returnTitle:
        return currName+str(addNum)

def getStickySaveNameList(includeExt=True):
    stickyList = []

    for File in os.listdir("SAVES/"):
        if File.endswith(".sticky"):
            if includeExt:
                stickyList.append(File)
            else:
                stickyList.append(File[:-7])
    
    return stickyList

def stringRemoveBadChars(string):
  allowed = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()[],-_"
  newString = ""
  for char in string:
    if char in allowed:
      newString += char
  return newString

def convertNewlines(string, direction=0):
    newString = ""
    # if direction is 0, then convert to newlines to \n
    # else, convert \n to the real character
    if direction == 0:
        newString = string.replace("\n", "\\n")
    elif direction == 1:
        newString = string.replace("\\n", "\n")

    return newString

def renameSticky(oldFilename, newTitle):
  f = open(oldFilename)
  oldContents = f.read()
  f.close()
  f = open("SAVES/"+stringRemoveBadChars(newTitle)+".sticky", "wt")
  f.write(oldContents)
  f.close()
  os.remove(oldFilename)

def getAllStickies():
    stickyList = []

    for File in os.listdir("SAVES/"):
        # get info from file and make sticky object
        if File.endswith(".sticky"):
            # open file
            f = open("SAVES/"+File, "rt")
            # get data first, then convert to json
            fileData = f.read()
            jsonData = json.loads(fileData)
            # set variables
            title, theme, content = jsonData["TITLE"], jsonData["THEME"], jsonData["CONTENT"]
            # convert newlines for content
            content = convertNewlines(content, direction=1)
            # make sticky object and append
            stickyList.append(classes.Sticky("SAVES/"+File, title, theme, content))

            """### debugging
            print(File)
            print(title)
            print(theme)
            print(content)"""
    
    return stickyList
