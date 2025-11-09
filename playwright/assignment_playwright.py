from playwright.sync_api import sync_playwright
import time

def main():
    # Define search query and output file
    search_query = "key functions in playwright in python"
    output_file = "chatgpt_metadata.txt"

    with sync_playwright() as p:
        # Launch browser (non-headless for visibility)
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context()
        page = context.new_page()

        # Step 1: Open ChatGPT
        page.goto("https://chat.openai.com", timeout=60000)
        print("Opened ChatGPT.")

        # Wait for page to load completely
        page.wait_for_timeout(5000)

        # Step 2: Type search query into search or chat box
        # Note: ChatGPT doesn’t have a public “search” field without login.
        # We'll simulate typing into the chat input.
        try:
            input_box = page.locator('xpath=//*[@id="prompt-textarea"]/p')
            input_box.click()
            input_box.fill(search_query)
            input_box.press("Enter")
            print("Search query sent.")
        except Exception as e:
            print("Could not find chat input box. You might need to log in manually.")
            print(e)

        # Optional: Wait for response (user may need to log in)
        page.wait_for_timeout(10000)

        # Step 3: Capture metadata
        metadata = {
            "title": page.title(),
            "url": page.url,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Step 4: Save metadata to text file
        with open(output_file, "w", encoding="utf-8") as f:
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")

        print(f"Metadata saved to {output_file}")

        # Close everything
        browser.close()

if __name__ == "__main__":
    main()
