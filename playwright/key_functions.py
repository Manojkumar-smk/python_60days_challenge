import asyncio
from playwright.async_api import async_playwright

async def run(playwright):
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto("https://google.com")
    await page.screenshot(path="ss1.png")
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)
        await asyncio.sleep(2)  # Wait for 2 seconds before closing

if __name__ == "__main__":
    asyncio.run(main())