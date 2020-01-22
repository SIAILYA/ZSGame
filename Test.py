import win32api

while True:
    cp = win32api.GetCursorPos()
    print(cp)
    if win32api.KeyPress('H'):
        break
