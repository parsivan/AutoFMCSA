import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def fetch_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://safer.fmcsa.dot.gov/query.asp?query_type=queryCarrierSnapshot&query_param=MC_MX&query_string=1714408")
        await page.wait_for_load_state("networkidle")
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")
        print(soup.prettify())
        await browser.close()

def main():
    asyncio.run(fetch_page())

if __name__ == "__main__":
    main()
