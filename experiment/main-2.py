import re
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


def main():
    # Initialize Chrome (make sure chromedriver is installed)
    driver = webdriver.Chrome(service=Service(
        "./chromedriver-linux64/chromedriver"))

    url = "https://safer.fmcsa.dot.gov/query.asp?query_type=queryCarrierSnapshot&query_param=MC_MX&query_string=1714408"
    driver.get(url)

    time.sleep(5)  # wait for JavaScript to load

    # Extract the rendered page HTML
    html = driver.page_sourcechromedriver  # Optional: parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())

    driver.quit()


def find():
    ...


if __name__ == "__main__":
    main()
