from playwright.sync_api import sync_playwright

def inspect_linkedin_job_classes(keyword="Python Developer", location="Chennai"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(storage_state="linkedin_state.json")
        page = context.new_page()

        # Open LinkedIn Jobs page
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}"
        page.goto(search_url, timeout=60000)
        print(f"🔍 Opened LinkedIn Jobs for '{keyword}' in '{location}'")

        # Wait for the jobs to load or for page elements to render
        page.wait_for_timeout(8000)

        # Capture all class names from <div> elements containing "job" (LinkedIn uses that in their CSS)
        all_classes = page.evaluate("""
        Array.from(document.querySelectorAll('div'))
            .map(el => el.className)
            .filter(cls => cls.includes('job'))
        """)

        # Remove duplicates and empty ones
        unique_classes = sorted(set(filter(None, all_classes)))

        print("\n🧩 Unique Job-related Classes Found:")
        for cls in unique_classes:
            print("-", cls)

        # Save a screenshot for reference
        page.screenshot(path="linkedin_class_inspect.png", full_page=True)
        print("\n📸 Screenshot saved: linkedin_class_inspect.png")

        browser.close()

if __name__ == "__main__":
    inspect_linkedin_job_classes("Python Developer", "Chennai")
