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
search_text = "Motor Vehicles"

carriers = []
output_data = []
soup = None


def read_file() -> None:
    """Read input csv file and store it in a list"""
    with open("input.csv") as f:
        r = csv.reader(f)
        for row in r:
            carriers.append({"ID": row[0], "name": row[1]})


def write_file(data: list) -> None:
    """Write the output data to a csv"""
    with open("output.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "Name", "Motor Vehicles"])
        writer.writeheader()
        writer.writerows(data)


async def fetch_page(url: str) -> None:
    """open the link with the key and id and export the html of the page to soup var"""
    global soup
    while True:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                await page.wait_for_load_state("networkidle")
                html = await page.content()
                soup = BeautifulSoup(html, "html.parser")  # Optional
                # print(soup.prettify())
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


def pick_key() -> str:
    """ask user to pick between mc and usdot number"""
    while True:
        print("Which ID type does your CSV contain?")
        print("1:", keys[0])
        print("2:", keys[1])
        choice = prompt("Enter 1 or 2: ").strip()
        if choice == "1":
            return keys[0]
        if choice == "2":
            return keys[1]
        print("Only enter 1 or 2.")


def yes_no_dialog(qstr: str) -> bool:
    """Ask the user for a YES or NO question. Returns True/False"""
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


def find_html(source: str) -> dict:
    """find option in the html and check if it has a value"""
    pattern = re.compile(
        rf'<td class="queryfield">\s*(.*?)\s*</td>\s*<td>.*?({re.escape(search_text)}).*?</td>',
        re.DOTALL,
    )
    if matches := pattern.search(source):
        option = {matches.group(2): matches.group(1)}
        return option


def boolify_options(options: dict) -> dict:
    value = options.get(search_text, "")
    options[search_text] = value == "X"
    return options
    # if options[search_text] == "X":
    #     options[search_text] = True
    #     return options
    # else:
    #     options[search_text] = False
    #     return options


async def process_carriers():
    key = pick_key()
    for carrier in carriers:
        cid = carrier["ID"]
        url = f"https://safer.fmcsa.dot.gov/query.asp?query_type=queryCarrierSnapshot&query_param={key}&query_string={cid}"

        await fetch_page(url)

        html = str(soup)
        found = find_html(html)
        if found:
            found = boolify_options(found)
            motor_val = found[search_text]
        else:
            motor_val = False

        output_data.append(
            {
                "ID": carrier["ID"],
                "Name": carrier["Name"],
                "Motor Vehicles": motor_val,
            }
        )


def main():
    read_file()
    asyncio.run(process_carriers())
    write_file(output_data)
    print("Done. Output saved to output.csv")


if __name__ == "__main__":
    main()
