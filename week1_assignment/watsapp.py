import pyautogui
import time
import webbrowser
from pathlib import Path
import sys

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.4

# Image template (a screenshot of the WhatsApp search bar)
TEMPLATE_IMAGE = "searchbar.png"  # place this in same folder as script
CONFIDENCE = 0.8  # works if opencv-python is installed

def main():
    # Step 1: Open WhatsApp Web
    webbrowser.open("https://web.whatsapp.com")
    print("Opening WhatsApp Web...")
    time.sleep(10)  # wait for page to load and QR to scan if needed

    # Step 2: Locate the search bar using image recognition
    print("Looking for WhatsApp search bar...")
    if not Path(TEMPLATE_IMAGE).exists():
        print(f"⚠️ Missing template image: {TEMPLATE_IMAGE}")
        print("Please capture a small screenshot of the search bar and save it as whatsapp_search_bar.png")
        sys.exit(1)

    try:
        search_location = pyautogui.locateOnScreen(TEMPLATE_IMAGE, confidence=CONFIDENCE)
    except TypeError:
        search_location = pyautogui.locateOnScreen(TEMPLATE_IMAGE)

    if search_location:
        center = pyautogui.center(search_location)
        pyautogui.moveTo(center.x, center.y, duration=0.3)
        pyautogui.click()
        print("✅ Search bar clicked.")
    else:
        print("❌ Could not find search bar on screen. Try recapturing image or adjusting confidence.")
        return

    # Step 3: Search for contact (replace with your test contact)
    pyautogui.typewrite("amma", interval=0.1)
    time.sleep(2)
    pyautogui.press("enter")

    # Step 4: Send message
    pyautogui.typewrite("Hello", interval=0.1)
    pyautogui.press("enter")

    print("✅ Message sent successfully (if search bar detected correctly).")

if __name__ == "__main__":
    main()
