import pygame
import functions as fcs
import classes as cs
import PygameTextWriter as pTW
import PygameKeyTracker as pKT

stickies, graphicalContainer, keyTracker, textWriter = (None, None, None, None)

def mainFcs():
  global stickies, graphicalContainer, keyTracker, textWriter

  def reset():
    graphicalContainer = cs.graphicalContainer((500, 350), fcs.rOA(stickies).mainColor, fcs.rOA(stickies).altColor1)
    fcs.rOA(stickies).resetIconPositions(graphicalContainer.res)
    keyTracker = pKT.KeyTracker(fcs.rOA(stickies).add, fcs.rOA(stickies).backspace, fcs.rOA(stickies).directionHandle, fps=fps)
    textWriter = pTW.TextWriter(graphicalContainer.surface, "FONT.png")
    pygame.display.set_caption(fcs.rOA(stickies).title)
  
  def loadStickies():
    fcsLoadedStickies = fcs.loadStickies()
    stickies = []
    for i in fcsLoadedStickies:
      stickies.append( cs.Sticky(loadStickies, returnStickies, changeActive, graphicalContainer, i) )
    stickies[0].active = True
    reset()
    keyTracker = pKT.KeyTracker(fcs.rOA(stickies).add, fcs.rOA(stickies).backspace, fcs.rOA(stickies).directionHandle, fps=fps)
  
  def returnStickies():
    return stickies
  
  def changeActive(title):
    fcs.rOA(stickies).menu = "CONTENT"
    for sticky in stickies:
      sticky.active = False
    for sticky in stickies:
      if sticky.title == title:
        sticky.active = True
        sticky.menu = "CONTENT"
    reset()

clock = pygame.time.Clock()
fps = 30

mainFcs.loadStickies()

running = True

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.VIDEORESIZE:
      graphicalContainer.resize((event.w, event.h))
      fcs.rOA(stickies).resetIconPositions(graphicalContainer.res)
    if event.type == pygame.MOUSEBUTTONDOWN:
      fcs.rOA(stickies).mouseDown()

  # draw background
  graphicalContainer.drawBackground()

  if fcs.rOA(stickies).menu == "CONTENT":  # content for sticky
    keyTracker.checkKeys()
    textWriter.write(fcs.rOA(stickies).content, fcs.rOA(stickies).margins, cursorPos=fcs.rOA(stickies).cursorPos)
    fcs.rOA(stickies).drawNumbers(textWriter)
  elif fcs.rOA(stickies).menu == "SETTINGS":  # content for settings menu
    fcs.rOA(stickies).drawSettings(graphicalContainer.surface, textWriter)
  elif fcs.rOA(stickies).menu == "OPEN":  # content for save picking
    fcs.rOA(stickies).drawSavePicker(graphicalContainer.surface, textWriter)

  # draw toolbar
  graphicalContainer.drawToolbar()
  # draw icons for current sticky note
  fcs.rOA(stickies).drawToolbarIcons(graphicalContainer.surface)
  # update display
  pygame.display.flip()
  # make sure we go at the fps rate
  clock.tick(fps)
