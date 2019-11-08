# sp500_data_spider.py

import os
import platform
import sys
import time
import json
import csv
import re

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def init_chrome_driver():
    # set selenium options
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)


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


def crawl_historic_data(driver, company_name):
    fieldnames = ["company_name", "market_date", "closing_price", "opening_price",
                  "highest_price", "lowest_price", "volume_in_millions", "percent_change"]
    filename = "./data/sp500data.csv"
    csv_file = None
    writer = None

    if os.path.exists(filename):
        csv_file = open(filename, "a")
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    else:
        csv_file = open(filename, "w+")
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

    currentTable = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "curr_table")))

    currentTable = currentTable.find_element_by_tag_name("tbody")
    entryRows = currentTable.find_elements_by_tag_name("tr")

    print("START scraping company : ", company_name)
    for entry in entryRows:
        company_entry = init_company_entry(company_name)
        entryDataKeys = list()
        dataPoints = entry.find_elements_by_tag_name("td")
        idx = 0
        for key in list(company_entry.keys())[1:]:
            entryDataKeys.append(key)
            data = dataPoints[idx].text

            if ("M" in data) & (key != "market_date"):
                data = data.replace('M', '')

            company_entry[key] = data
            idx += 1
        writer.writerow(company_entry)
        # print(company_entry)
        # time.sleep(1)
    print("DONE scraping company : ", company_name)


def crawl_company_urls(driver, sp500Urls):
    for key in sp500Urls:
        company_name = key
        companyUrl = sp500Urls[company_name] + '-historical-data'
        print("name : ", company_name)
        print("url  : ", companyUrl, "\n")
        driver.get(companyUrl)

        # select data spanning past 10 years
        historicDates = "'01/01/2009 - 01/01/2019'"
        jsSetPicker = "document.getElementById('picker').value = "
        jsSetPicker = jsSetPicker + historicDates
        driver.execute_script(jsSetPicker)

        # ElementClickInterceptedException

        selectPicker = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "widgetField")))

        selectPicker.click()

        # elementBlocked = True
        # max_retries = 20
        # while elementBlocked & max_retries > 0:
        #     print("retry ", max_retries)
        #     try:
        #         selectPicker.click()
        #         elementBlocked = False
        #     except:
        #         time.sleep(1)
        #     finally:
        #         max_retries -= 1

        applyButton = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "applyBtn")))

        applyButton.click()
        crawl_historic_data(driver, company_name)


if __name__ == "__main__":

    # grab the urls we saved using the url spider
    sp500Urls = list()
    with open("urls/sp500Urls_01.json", "r") as read_file:
        sp500Urls = json.load(read_file)

    with init_chrome_driver() as driver:
        crawl_company_urls(driver, sp500Urls)
        driver.quit()
