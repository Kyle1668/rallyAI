"""
sp500_data_spider.py
--------------------

Crawls over the S&P top 500 companies, gathering 10 years of historic data.
Log output by redirecting stdout to a file to see where things left off.
"""

import os
import platform
import sys
import time
import json
import csv
import re
from datetime import datetime
from datetime import timedelta

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def init_chrome_driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

def load_historic_data_table():
    def getTenYearTimeSpanString():
        currentDate = datetime.now()
        year = timedelta(days=365)
        ten_years = 10 * year
        tenYearsAgo = currentDate - ten_years
        timeSpanStr = "'" + \
            tenYearsAgo.strftime("%m/%d/%Y") + \
            " - " + \
            currentDate.strftime("%m/%d/%Y") + \
            "'"
        return timeSpanStr
    
    # select data spanning the past 10 years
    historicDates = getTenYearTimeSpanString()
    jsSetPicker = "document.getElementById('picker').value = "
    jsSetPicker = jsSetPicker + historicDates
    driver.execute_script(jsSetPicker) # sets the values

    # apply date selection to date picker
    selectPicker = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "widgetField")))
    selectPicker.click() # reveals the date picker

    applyButton = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "applyBtn")))

    retries = 5
    while(retries > 0):
        try: # keep trying to click apply
            applyButton.click()
            retries = 0
        except ElementClickInterceptedException:
            print("apply button wasn't clicked")
            retries -= 1

def init_company_entry(company_name):
    company_entry = {}
    company_entry["company_name"] = company_name
    company_entry["market_date"] = ""
    company_entry["closing_price"] = ""
    company_entry["opening_price"] = ""
    company_entry["highest_price"] = ""
    company_entry["lowest_price"] = ""
    company_entry["volume_in_millions"] = ""
    company_entry["percent_change"] = ""
    return company_entry

def parse_table_rows(rows, company_name):
    company_entries = list()
    for row in rows:
        company_entry = init_company_entry(company_name)
        entryDataKeys = list()
        data_points = row.find_all("td")
        idx = 0
        for key in list(company_entry.keys())[1:]:
            entryDataKeys.append(key)
            data = data_points[idx].get_text()
            company_entry[key] = data
            idx += 1
        company_entries.append(company_entry)
    return company_entries


def crawl_historic_data(driver, company_name):
    retries = 5
    while(retries > 0):
        try:  # waiting for the table to fully load
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "curr_table")))
            retries = 0
        except TimeoutException:
            print("timeout exception occured on current table")
            retries -= 1

    # parse the page source to get the table rows
    currPageSource = driver.page_source
    soup = BeautifulSoup(currPageSource, 'html.parser')
    table = soup.find("table", {"id": "curr_table"})
    tbody = table.contents[3]
    trows = tbody.find_all("tr")
    company_entries = parse_table_rows(trows, company_name)

    # print to stdout for debugging
    print("company name : ", company_name, " : ",
          datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("number of entries : ", len(company_entries))
    print("DONE scraping company : ", company_name)

    return company_entries


def crawl_company_urls(driver, sp500Urls):
    fieldnames = ["company_name", "market_date", "closing_price", "opening_price",
                  "highest_price", "lowest_price", "volume", "percent_change"]

    # file variables
    filename = "./data/sp500data.csv"
    csv_file = None
    writer = None

    if os.path.exists(filename):  # append to existing data
        csv_file = open(filename, "a")
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    else:  # generate new csv data file with headers
        csv_file = open(filename, "w+")
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

    for key in sp500Urls:
        company_name = key
        companyUrl = sp500Urls[company_name] + '-historical-data'

        # print to stdout for debugging
        print("company name      : ", company_name)
        print("historic data url : ", companyUrl, "\n")

        driver.get(companyUrl) # navigate to company url
        load_historic_data_table()
        company_entries = crawl_historic_data(driver, company_name)

        for entry in company_entries:
            writer.writerow(entry)
        
    csv_file.close()

if __name__ == "__main__":

    sp500Urls = list()
    with open("urls/sp500_urls.json", "r") as urlFile:
        sp500Urls = json.load(urlFile)

    with init_chrome_driver() as driver:
        crawl_company_urls(driver, sp500Urls)
        driver.quit()
