from playwright.sync_api import sync_playwright

def save_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.linkedin.com/login")
        print("🔑 Please log in manually. Close the browser when done.")
        page.wait_for_timeout(30000)  # Wait 30 sec for manual login
        context.storage_state(path="linkedin_state.json")
        print("✅ Session saved to linkedin_state.json")
        browser.close()

if __name__ == "__main__":
    save_session()
