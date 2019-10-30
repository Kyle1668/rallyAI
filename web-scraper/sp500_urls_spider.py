# stocks_scraper.py

import os
import platform
import sys
import time

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

if __name__ == "__main__":
    url = 'https://www.investing.com/equities/'
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(options=options)
    browser.get(url)

    optionSelector = browser.find_element_by_id('stocksFilter')
    options = optionSelector.find_elements_by_tag_name('option')
    optionToSelect = None

    for option in options:
        if option.text == 'S&P 500':
            optionToSelect = option
            break

    option.click()
    time.sleep(10)

    sp500StockTable = browser.find_element_by_id('cross_rate_markets_stocks_1')
    sp500StockTable = sp500StockTable.find_element_by_tag_name('tbody')

    sp500Urls = {}

    sp500StockRows = sp500StockTable.find_elements_by_tag_name('tr')

    for row in sp500StockRows:
        entry = row.find_elements_by_tag_name('td')[1]
        entryLink = entry.find_element_by_tag_name('a')
        entryUrl = entryLink.get_attribute('href')
        entryName = entryLink.text
        sp500Urls[entryName] = entryUrl
        # print("entry : ", entryName)
        # print("url : ", entryUrl)

    print(sp500Urls)

    browser.quit()
