import pygame

disp = pygame.display.set_mode((200, 200))
running = True

pygamePressedKeys = []
normalLetters = []

while running:
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
      running = False
    elif event.type == pygame.KEYDOWN:
      pygamePressedKeys.append(event.key)

print("Pygame Pressed Keys:")
print(pygamePressedKeys)
print("Normal Letters:")
print(normalLetters)
