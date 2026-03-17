import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        await page.goto("https://www.investing.com/holiday-calendar/", timeout=60000)
        
        with open("body.html", "w") as f:
            f.write(await page.content())

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
