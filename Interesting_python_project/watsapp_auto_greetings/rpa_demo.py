import pyautogui
import time

import mousepointer

# time.sleep(2)
# pyautogui.rightClick(100, 100)

# time.sleep(3)
# x, y = mousepointer.get_mouse_position()
# pyautogui.click(x,y)
# print(f"Clicked at position: ({x}, {y})")

# pyautogui.scroll(500)

# pyautogui.typewrite("python rpa_demo.py", interval=0.1)
# pyautogui.typewrite("Hello World!", interval=0.1)

# pyautogui.press("enter")

# pyautogui.hotkey("ctrl", "a")
# pyautogui.hotkey("ctrl", "c")

time.sleep(3)
x, y = mousepointer.get_mouse_position()
pyautogui.click(x,y)
print(f"Clicked at position: ({x}, {y})")

# pyautogui.hotkey("ctrl", "v")


#image recognition

# location = pyautogui.locateOnScreen("chat.png")
# print(location)
# # pyautogui.click(location)
# # pyautogui.center(location)
# pyautogui.click(pyautogui.center(location))

# pyautogui.size()  # returns (width, height) of the screen.
# print(pyautogui.size())

# pyautogui.screenshot("screenshot.png")  # takes screenshot and saves it to a file.
