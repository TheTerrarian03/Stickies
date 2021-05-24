import pynput, time, os

pressed = []
running = True

def on_press(key):
  global pressed
  try:
    if not key.char in pressed:
      pressed.append(key.char)
  except:
    pass

def on_release(key):
  global pressed
  try:
    if key.char in pressed:
      pressed.remove(key.char)
  except:
    pass

def on_click(x, y, button, pressed):
  global running
  running = False

kbrd = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
mouse = pynput.mouse.Listener(on_click=on_click)
kbrd.start()
mouse.start()

while True:
  os.system("clear")
  print(pressed)
  time.sleep(0.05)
