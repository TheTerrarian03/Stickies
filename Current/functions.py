from posixpath import curdir
import classes
import os

def lineToLowercase(string, line):
    print(string, line)

def lineToUppercase(string, line):
    print(string, line)

def returnOnlyActive(objList):
    for obj in objList:
        if obj.active:
            return obj

def rOA(objList):
  return returnOnlyActive(objList)

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

def makeNewSticky(returnTitle=False):
    currName = "NewSticky"
    addNum = 1
    looping = True

    while looping:
        if not os.path.exists("SAVES/"+currName+str(addNum)+".sticky"):
            toWrite = "/TITLE " + currName + str(addNum) + "\n/THEME YELLOW\n/START-CONTENT\nWelcome to the your sticky!\nComplain about life here! Or make a to do list.\nOr, do whatever!\n\nEnjoy.\n-Logan Meyers :)\n/END-CONTENT\n"
            f = open("SAVES/"+currName+str(addNum)+".sticky", "wt")
            f.write(toWrite)
            f.close()
            looping = False
        else:
            addNum += 1
    
    if returnTitle:
        return currName+str(addNum)

def getStickySaveNameList():
    stickyList = []

    for File in os.listdir("SAVES/"):
        if File.endswith(".sticky"):
            stickyList.append(File)
    
    return stickyList

def getAllStickies():
    stickyList = []

    for File in os.listdir("SAVES/"):
        # get info from file and make sticky objects
        if File.endswith(".sticky"):
            title, theme, content = None, None, ""
            cs = False
            done = False
            f = open("SAVES/"+File, "rt")
            for line in f:
                lineS = line.split(" ")
                if lineS[0] == "/TITLE":
                    title = lineS[1]
                elif lineS[0] == "/THEME":
                    theme = lineS[1]
                elif lineS[0] == "/START-CONTENT\n":
                    cs = True
                elif lineS[0] == "/END-CONTENT\n":
                    cs = False
                    done = True
                else:
                    if cs and not done:
                        content += line
            # remove newlines
            title = title[:-1]
            if theme.endswith("\n"):
                theme = theme[:-1]
            # make sticky object and append
            stickyList.append(classes.Sticky("SAVES/"+File, title, theme, content))
    
    return stickyList
