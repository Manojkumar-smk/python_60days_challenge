# open_search_click.py  (Keyboard method)
import time
import webbrowser
import platform
import pyautogui

pyautogui.FAILSAFE = True  # move mouse to top-left to abort
pyautogui.PAUSE = 0.15     # small pause after each PyAutoGUI call

# Config - adjust if needed
QUERY = "south africa vs australia score"
SEARCH_URL = "https://www.google.com"  # open Google first
TAB_PRESSES = 7   # number of Tab presses to reach first result; adjust if needed
DELAY_AFTER_OPEN = 3.0  # seconds to wait for browser to open
DELAY_AFTER_SEARCH = 2.5  # seconds to wait after typing search

# Use platform-specific key for focusing address bar
system = platform.system().lower()
if system == "darwin":
    focus_addr_hotkey = ("command", "l")
else:
    focus_addr_hotkey = ("ctrl", "l")

def main():
    print("Opening browser...")
    webbrowser.open(SEARCH_URL)
    time.sleep(DELAY_AFTER_OPEN)

    print("Focusing address bar and typing query...")
    pyautogui.hotkey(*focus_addr_hotkey)
    time.sleep(0.25)
    pyautogui.typewrite(QUERY, interval=0.04)
    pyautogui.press("enter")

    time.sleep(DELAY_AFTER_SEARCH)

    print(f"Pressing Tab {TAB_PRESSES} times to reach first result (adjust TAB_PRESSES if necessary)...")
    for i in range(TAB_PRESSES):
        pyautogui.press("tab")
        time.sleep(0.12)
    pyautogui.press("enter")
    print("Done — first result should be opened.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
