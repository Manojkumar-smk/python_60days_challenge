import pyautogui
import PyPDF2
import time
import os

def open_pdf_on_desktop(filename):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    pdf_path = os.path.join(desktop_path, filename)

    # Open Run dialog (Windows + R)
    pyautogui.hotkey('win', 'r')
    time.sleep(1)

    # Type full path and open
    pyautogui.write(pdf_path)
    pyautogui.press('enter')
    time.sleep(3)  # Wait for PDF viewer to open

    return pdf_path

def count_word_in_pdf(pdf_path, target_word):
    count = 0
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    count += text.lower().split().count(target_word.lower())
        return count
    except Exception as e:
        print(f"Error: {e}")
        return -1

if __name__ == "__main__":
    pdf_name = input("Enter PDF filename (e.g., report.pdf): ")
    search_word = input("Enter word to count: ")

    pdf_path = open_pdf_on_desktop(pdf_name)
    result = count_word_in_pdf(pdf_path, search_word)

    if result >= 0:
        print(f"The word '{search_word}' appears {result} times in '{pdf_name}'.")
    else:
        print("Failed to process the PDF.")