import asyncio
from playwright.async_api import async_playwright
import csv
from bs4 import BeautifulSoup

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        print("Navigating to Investing.com Holiday Calendar...")
        await page.goto("https://www.investing.com/holiday-calendar/", timeout=60000)
        
        print("Fetching all countries from UI...")
        options = await page.evaluate('''() => {
            const select = document.getElementById("countrySelectDropdown");
            return Array.from(select.options).map(opt => ({
                id: opt.value,
                name: opt.text
            }));
        }''')
        countries = [opt for opt in options if opt['id'] and int(opt['id']) > 0]
        print(f"Total countries found: {len(countries)}")

        # For the fetch API, we can either pass an array of countries or no country parameter to potentially get all of them.
        # But looping might be safer to avoid timeouts or limits.
        
        with open("holidays_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Country", "Exchange", "Holiday"])

        for c in countries:
            print(f"Fetching data for {c['name']} (ID: {c['id']})...")
            html_table_rows = await page.evaluate(f'''async () => {{
                try {{
                    const formData = new URLSearchParams();
                    formData.append('country[]', '{c['id']}');
                    formData.append('dateFrom', '2024-01-01');
                    formData.append('dateTo', '2025-12-31');
                    formData.append('currentTab', 'custom');
                    formData.append('limit_from', '0');
                    
                    const response = await fetch('/holiday-calendar/Service/getCalendarFilteredData', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-Requested-With': 'XMLHttpRequest'
                        }},
                        body: formData.toString()
                    }});
                    const data = await response.json();
                    return data.data; // HTML rows
                }} catch (e) {{
                    return null;
                }}
            }}''')
            
            if not html_table_rows:
                print(f"  No data or error for {c['name']}")
                continue
                
            soup = BeautifulSoup(html_table_rows, "html.parser")
            rows = soup.find_all("tr")
            
            records = []
            current_date = None
            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 4:
                    date_text = cols[0].text.strip()
                    if date_text:
                        current_date = date_text
                    
                    country = cols[1].text.strip()
                    exchange = cols[2].text.strip()
                    holiday = cols[3].text.strip()
                    
                    records.append([current_date, country, exchange, holiday])

            if records:
                with open("holidays_data.csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerows(records)
                print(f"  -> Saved {len(records)} holidays.")
            
            # Short sleep to prevent rate limiting
            await asyncio.sleep(0.5)

        await browser.close()
        print("Scraping finished successfully!")

if __name__ == "__main__":
    asyncio.run(main())
