import pygame
import functions as fcs
import classes as cs
import PygameTextWriter as pTW
import PygameKeyTracker as pKT

# starting info
info  = cs.Info(30)
running = True

# set icon
pygame.display.set_icon(pygame.image.load("ICON.png"))

# main while loop
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.VIDEORESIZE:
      info.dispObj.resize((event.w, event.h))
      fcs.rOA(info.stickies).resetIconPositions()
    if event.type == pygame.MOUSEBUTTONDOWN:
      fcs.rOA(info.stickies).mouseDown()

  # draw background
  info.dispObj.drawBackground()

  if fcs.rOA(info.stickies).menu == "CONTENT":  # content for sticky
    info.keyTracker.checkKeys()
    info.textWriter.write(fcs.rOA(info.stickies).content, fcs.rOA(info.stickies).margins, cursorPos=fcs.rOA(info.stickies).cursorPos)
    fcs.rOA(info.stickies).drawNumbers()
  elif fcs.rOA(info.stickies).menu == "SETTINGS":  # content for settings menu
    fcs.rOA(info.stickies).drawSettings()
  elif fcs.rOA(info.stickies).menu == "OPEN":  # content for save picking
    fcs.rOA(info.stickies).drawSavePicker()

  # draw toolbar
  info.dispObj.drawToolbar()
  # draw icons for current sticky note
  fcs.rOA(info.stickies).drawToolbarIcons()
  # update display
  pygame.display.flip()
  # make sure we go at the fps rate
  info.clock.tick(info.fps)
