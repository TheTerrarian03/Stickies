import pygame
import classes as cs
import functions as fcs

running = True
saveLoc, mainCol, altCol1, altCol2, defTitle, fontImg, fps, assetsFolder = fcs.loadSettings("SETTINGS")
# print(saveLoc, mainCol, altCol, defTitle, fontPath)
mainWin = cs.display(defTitle, mainCol, altCol1)
stickies = []
for save in fcs.getSavesList(saveLoc):
  stickies.append(cs.sticky(mainWin, (saveLoc + "/" + save), False, assetsFolder, fontImg, altCol2))
stickies[0].setActive()
# alternate:
# stickies[0].setInactive()
clock = pygame.time.Clock()

# debug stuff no touchy ok?
print(stickies)
for sticky in stickies:
  print(sticky)
  for icon in sticky.icons:
    print(" " + icon + ": " + str(sticky.icons[icon]))

while running:
  eventc = 0
  eventcLimit = 60
  for event in pygame.event.get():
    if not event:
      eventc += 1
    else:
      eventc = 0
     
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.VIDEORESIZE:
      mainWin.resize(event.size)
    elif event.type == pygame.VIDEOEXPOSE:
      print("exposed or smth")
    fcs.returnOnlyActive(stickies).eventCheck(event)
  
  if eventc < eventcLimit:
    mainWin.draw()
    fcs.returnOnlyActive(stickies).draw(mainWin.surface)
    pygame.display.flip()
  
  # print(eventd)
  
  # wait
  clock.tick(fps)

