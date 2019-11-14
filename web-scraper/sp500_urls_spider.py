# sp500_urls_spider.py

import os
import platform
import sys
import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

if __name__ == "__main__":
    url = 'https://www.investing.com/equities/'
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    optionSelector = driver.find_element_by_id('stocksFilter')
    options = optionSelector.find_elements_by_tag_name('option')
    optionToSelect = None

    for option in options:
        if option.text == 'S&P 500':
            optionToSelect = option
            break

    option.click()
    # time.sleep(10)
    sp500StockTable = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "cross_rate_markets_stocks_1")))
    #sp500StockTable = driver.find_element_by_id('cross_rate_markets_stocks_1')
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

    driver.quit()
