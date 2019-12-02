import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pytest


@pytest.fixture
def init_chrome_driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)


def test_chrome_driver(init_chrome_driver):
    driver = init_chrome_driver
    driver.get("https://www.lambdatest.com/")
    title = driver.title
    print(f'what is my title ? : {title}')
    driver.quit()
    assert title == 'Cross Browser Testing Tools | Free Automated Website Testing | LambdaTest'


def test_parse_table_rows(init_chrome_driver):
    from sp500_data_spider import parse_table_rows
    page_source = None
    with open('./mock/mock_html', 'r') as mock_html:
        page_source = mock_html.read()
    soup = BeautifulSoup(page_source, 'html.parser')
    table = soup.find("table", {"id": "curr_table"})
    tbody = table.contents[3]
    trows = tbody.find_all("tr")
    company_entries = parse_table_rows(trows[:3], 'test_company')
    print(f'{company_entries}')
    assert company_entries
