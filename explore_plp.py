import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating to PLP...")
        await page.goto("https://plp.moeys.gov.kh/teacher-attendance", wait_until="networkidle")
        title = await page.title()
        
        # Save HTML to see the DOM structure
        content = await page.content()
        with open("plp_login.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print("Saved login page to plp_login.html")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
