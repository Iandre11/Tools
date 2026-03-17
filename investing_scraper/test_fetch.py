import asyncio
from playwright.async_api import async_playwright
import time

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        print("Navigating...")
        await page.goto("https://www.investing.com/holiday-calendar/", timeout=60000)
        
        # Now evaluate fetch
        print("Fetching data from API...")
        html = await page.evaluate('''async () => {
            const formData = new URLSearchParams();
            // Let's try passing multiple countries or no country
            // formData.append('country[]', '5'); // USA
            // formData.append('country[]', '32'); // Spain
            formData.append('dateFrom', '2024-01-01');
            formData.append('dateTo', '2025-12-31');
            formData.append('currentTab', 'custom');
            formData.append('limit_from', '0');
            
            const response = await fetch('/holiday-calendar/Service/getCalendarFilteredData', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData.toString()
            });
            const data = await response.json();
            return data.data; // usually HTML string
        }''')
        
        print("Success! Length of HTML:", len(html) if html else "None")
        with open("fetch_result.html", "w") as f:
            f.write(html if html else "")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
