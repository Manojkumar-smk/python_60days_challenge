from playwright.sync_api import sync_playwright
import pandas as pd
import time
import logging

def linkedin_job_scraper(keyword="SAP ABAP Developer", location="India"):
    logging.basicConfig(level=logging.INFO)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(storage_state="linkedin_state.json")
        page = context.new_page()

        search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}"
        page.goto(search_url, timeout=60000)
        logging.info(f"🔍 Searching for '{keyword}' jobs in '{location}'...")

        try:
            page.wait_for_selector(".jobs-search-results-list", timeout=10000)
        except:
            logging.warning("⚠️ Job list not found. Check login or page structure.")
            browser.close()
            return

        # Scroll to load more jobs
        for _ in range(3):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(2000)

        # Extract job cards
        job_cards = page.locator("ul.jobs-search__results-list li")
        data = []

        for i in range(job_cards.count()):
            card = job_cards.nth(i)
            title = card.locator("a.job-card-list__title, a.job-card-container__link").inner_text()
            company = card.locator("span.job-card-container__primary-description").inner_text()
            location = card.locator("li.job-card-container__metadata-item").inner_text()
            link = card.locator("a.job-card-list__title, a.job-card-container__link").get_attribute("href")

            data.append({
                "Title": title.strip(),
                "Company": company.strip(),
                "Location": location.strip(),
                "Link": f"https://www.linkedin.com{link}" if link and link.startswith("/jobs") else link
            })

        # Save to CSV
        df = pd.DataFrame(data)
        df.drop_duplicates(subset="Link", inplace=True)
        df = df[df["Title"] != ""]

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"linkedin_sap_abap_jobs_{timestamp}.csv"
        df.to_csv(file_name, index=False, encoding="utf-8-sig")

        logging.info(f"✅ Saved {len(df)} jobs to '{file_name}'")
        browser.close()

if __name__ == "__main__":
    linkedin_job_scraper()
