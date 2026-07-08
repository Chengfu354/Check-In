import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()
USERNAME = os.getenv("PLP_USERNAME")
PASSWORD = os.getenv("PLP_PASSWORD")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Navigating to PLP...")
        await page.goto("https://plp.moeys.gov.kh/teacher-attendance", wait_until="networkidle")
        
        print("Logging in...")
        await page.fill("#userName", USERNAME)
        await page.fill("#password", PASSWORD)
        await page.click(".login-submit-btn")
        
        # Wait for navigation or a specific element that appears after login
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(2) # just to be safe
        
        # Dump the HTML after login
        content = await page.content()
        with open("plp_dashboard.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print("Saved dashboard page to plp_dashboard.html")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
