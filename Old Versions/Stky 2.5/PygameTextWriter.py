import pygame, time

class TextWriter:
    def __init__(self, dispSurface, color, pt=12, font="Monospace", blinkingCursor=True):
        # pygame font init
        pygame.font.init()
        # variables passed in
        self.dispSurface = dispSurface
        self.font = font
        self.pt = pt
        self.oriPt = pt
        self.color = color
        self.blinkingCursor = blinkingCursor
        # variables to be figured out
        self.charDims = [0, 0]
        self.vertSpacing = 0
        self.cursorWid = 1
        # pygame font obj
        self.fontMaker = pygame.font.SysFont(self.font, self.pt)
        # initializing function calls
        self.setRefDims()

    def setRefDims(self):
        singleChar = self.fontMaker.render("E", True, self.color)
        self.charDims = [singleChar.get_rect()[2], singleChar.get_rect()[3]]
    
    def scale(self, newScale):
        try:
            int(self.oriPt*newScale)
        except TypeError:
            print("TextWriter ERROR: 'newScale' needs to be an INT!")
        self.pt = int(self.oriPt * newScale)
        self.cursorWid = 1*newScale
        self.fontMaker = pygame.font.SysFont(self.font, self.pt)
        self.setRefDims()
    
    def calcBlink(self):
        if self.blinkingCursor:
            if time.time() % 1 > 0.5:
                return True
            return False
        return True

    def write(self, text, margins, cursorPos=None, splitAtNewline=True):
        if splitAtNewline:
            cursorDrawn, contentLoc, x, y = False, 0, margins[0], margins[1]
            for char in text:
                if contentLoc == cursorPos and self.calcBlink():
                    pygame.draw.rect(self.dispSurface, self.color, (x, y, self.cursorWid, self.charDims[1]))
                    cursorDrawn = True
                if char == "\n":
                    x = margins[0]
                    y += self.charDims[1]
                elif char == " ":
                    x += self.charDims[0]
                else:
                    textRect = self.fontMaker.render(char, True, self.color)
                    self.dispSurface.blit(textRect, (x, y))
                    x += self.charDims[0]
                contentLoc += 1
            if not cursorDrawn and self.calcBlink() and cursorPos:
                pygame.draw.rect(self.dispSurface, self.color, (x, y, self.cursorWid, self.charDims[1]))
        else:
            # replace "\n" with "\\n"
            newText = text.replace("\n", "\\n")
            # print(newText)
            textRect = self.fontMaker.render(newText, True, self.color)
            self.dispSurface.blit(textRect, (0, 0))
