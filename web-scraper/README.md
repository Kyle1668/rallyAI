# web-scraper

## info

webscraper we'll be using to gather data on market trends

## dependencies

Python : version = 3.7.4

`python3 -m pip install --user virtualenv`

`python3 -m venv env`

`pip3 install -r requirements.txt`

## usage

### sp500 urls spider

Run the urls spider using python3 and redirect the output to either a .json or .jl file

`python3 sp500_urls_spider.py > urls/sp500Urls.jl`

### sp500 data spider

company_name
market_date
closing_price
opening_price
highest_price
lowest_price
volume_in_millions

## Selenium Notes

useful exceptions : ElementClickInterceptedException
