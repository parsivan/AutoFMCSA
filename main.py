#!/usr/bin/env python
import sys
import re
import csv
import subprocess
import asyncio
import logging

from playwright.async_api import async_playwright, Error
from bs4 import BeautifulSoup

import getpass
from prompt_toolkit import prompt

"""
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
"""

keys = ("MC_MX", "USDOT")
carriers = []
soup = None
url = f"https://safer.fmcsa.dot.gov/query.asp?query_type=queryCarrierSnapshot&query_param={key}&query_string={id}"


def read_file():
    with open("mc-number.csv") as f:
        r = csv.reader(f)
        for row in r:
            carriers.append({"ID": row[0], "name": row[1]})


async def fetch_page():
    while True:
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
                print("Error: Playwright has no browsers installed")
                # time.sleep(1)
                answer = yes_no_dialog(
                    "Do you want this script to run 'playwright install' command"
                )
                if answer:
                    try:
                        subprocess.run(["playwright", "install"], check=True)
                    except subprocess.CalledProcessError as er:
                        print(f"Installation failed with exit code {er.returncode}")
                        print(f"Command that failed: {er.cmd}")
                        sys.exit(1)
                    continue
                else:
                    print("Exiting Program")
                    sys.exit(1)


def yes_no_dialog(qstr: str) -> bool:
    """ "Ask the user for a YES or NO question. Returns True/False"""
    while True:
        answer = prompt(
            message=qstr,
            default=f"{getpass.getuser().strip().lower()}",
        )
        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no"]:
            return False
        else:
            print("Please only type y/yes or n/no")


def find():
    re.search()


def main(): ...


if __name__ == "__main__":
    main()
