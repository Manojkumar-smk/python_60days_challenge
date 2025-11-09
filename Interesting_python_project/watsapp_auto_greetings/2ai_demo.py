import pyautogui
import time
import webbrowser

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3  # small delay between actions

# Step 1: Open Gmail
webbrowser.open("https://mail.google.com")
time.sleep(5)  # wait for Gmail to load

# Step 2: Click on Compose button
# ⚠️ Adjust these coordinates for your screen!
# To find coordinates: run pyautogui.position() in a Python shell and hover over "Compose"
pyautogui.click(150, 200)  # Example position for Compose button
time.sleep(2)

# Step 3: Type recipient email
pyautogui.typewrite("manojkumar.smk09@outlook.com", interval=0.05)
pyautogui.press("tab")  # move to subject field
time.sleep(0.5)

# Step 4: Type subject
pyautogui.typewrite("Automated Email from PyAutoGUI", interval=0.05)
pyautogui.press("tab")  # move to body
time.sleep(0.5)

# Step 5: Type body text
pyautogui.typewrite("Hello Manoj,\n\nThis is an automated test email sent using PyAutoGUI.\n\nRegards,\nPython Bot", interval=0.05)
time.sleep(0.5)

# Step 6: Send email (Ctrl + Enter)
pyautogui.hotkey("ctrl", "enter")

print("✅ Email sent successfully (if coordinates were correct).")
