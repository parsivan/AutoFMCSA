import json
import csv
import requests
from bs4 import BeautifulSoup

url = "https://safer.fmcsa.dot.gov/query.asp?query_type=queryCarrierSnapshot&query_param=MC_MX&query_string=1714408"

def main():
    response = requests.get(url)

    print(response.status_code)
    print(response.text[:500])  # inspect the HTML

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
    # then find the relevant tables or fields and extract desired values

if __name__ == "__main__":
    main()
