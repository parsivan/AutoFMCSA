import sys
import re
import csv
import subprocess
import asyncio
import logging

from playwright.async_api import async_playwright, Error
from bs4 import BeautifulSoup

from prompt_toolkit import prompt

system = sys.platform
if system.startswith("win"):
    chromedriver = "./chromedriver-win64/chromedriver.exe"
elif system.startswith("linux"):
    chromedriver = "./chromedriver-linux64/chromedriver"
else:
    try:
        raise OSError("Operating System not supported")
    except OSError as e:
        print(e)
        exit(1)


carriers = []
soup = None
url = f"https://safer.fmcsa.dot.gov/query.asp?query_type=queryCarrierSnapshot&query_param=MC_MX&query_string=1714408"


def read_file():
    with open("mc-number.csv") as f:
        r = csv.reader(f)
        for row in r:
            carriers.append({"name": row[0], "ID": row[1]})


async def fetch_page():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.wait_for_load_state("networkidle")
            html = await page.content()
            # Optional: parse HTML with BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            print(soup.prettify())
            await browser.close()
    except Error as e:
        if "playwright install" in str(e):
            print()
            subprocess.run(["playwright", "install"], check=True)
            # p


def find():
    ...


def main():
    ...


if __name__ == "__main__":
    main()
