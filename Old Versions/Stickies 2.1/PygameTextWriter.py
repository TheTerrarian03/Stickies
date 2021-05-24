import pygame

DEF_FONT_INFO = [[5, 7, 2, 2], 1, "0123456789.ABCDEFGHIJKLMNOPQRSTUVWXYZ-,\"\'abcdefghijklmnopqrstuvwxyz`~!@#$%^&*()_[]{};:\\|<>/?=+"]
# items: [(wid, hi, horizMargin, vertiMargin), scale, [o, r, d, e, r, etc]

class TextWriter:
  def __init__(self, dispSurface, fontImagePath, fontInfo=DEF_FONT_INFO):
    self.dispSurface = dispSurface
    self.fontInfo = fontInfo
    self.fontImg = pygame.image.load(fontImagePath)
  
  def write(self, content, margins, cursorPos=None, debug=False):
    x = margins[0]
    y = margins[1]
    contentLoc = 0
    cursorDrawn = False
    if debug:
      print("Starting Drawing Content")
    for char in content:
      if contentLoc == cursorPos:
        pygame.draw.rect(self.dispSurface, (25, 25, 25), (x, y, self.fontInfo[0][0], self.fontInfo[0][1]))
        x += self.fontInfo[0][0]+self.fontInfo[0][2]
        cursorDrawn = True
      elif char == " ":
        x += self.fontInfo[0][0]+self.fontInfo[0][2]
      else:
        # for non-space characters
        self.dispSurface.blit(self.fontImg, (x, y), area=((self.fontInfo[2].find(char)*self.fontInfo[0][0]), 0, self.fontInfo[0][0], self.fontInfo[0][1]))
        if debug:
          print(self.fontImg, (x, y), ((self.fontInfo[2].find(char)*self.fontInfo[0][0]), 0, self.fontInfo[0][0], self.fontInfo[0][1]))
        x += self.fontInfo[0][0]+self.fontInfo[0][2]
      if char == "\n":
        x = margins[0]
        y += self.fontInfo[0][1]+self.fontInfo[0][3]
      contentLoc += 1
    if not cursorDrawn and cursorPos:
      pygame.draw.rect(self.dispSurface, (25, 25, 25), (x, y, self.fontInfo[0][0], self.fontInfo[0][1]))
    if debug:
      print("Done Drawing Content")