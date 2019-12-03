# web-scraper

## info

web-scraper contains two web scraping 'crawlers': `sp500_data_spider.py` and `sp500_urls_spider.py`

`sp500_urls_spider.py` retrieves the urls for each of the sp500 comapnies from investing.com and writes

the result to a json object containing the company name as a key and the url as it's value. This json

is then saved to a file named 'urls/sp500_urls.json'.


The `sp500_data_spider.py` grabs the file containing the urls to scrape historic data for each of the

companies contained in the 'urls/sp500_urls.json' file. The scraper loads a historic data table for

each company and collects data over a time span of ten years ago from the current date. All this data

gets saved to one large .csv file under 'data/sp500data.csv'.


## dependencies and installation

Python : version = 3.7.4

`python3 -m pip install --user virtualenv`

`python3 -m venv env`

`pip3 install -r requirements.txt`

You must also install the latest **chromedriver** and save the location of the driver to your `$PATH`

## usage

### sp500 urls spider

Run the urls spider using python3 and redirect the output to either a .json or .jl file

`python3 sp500_urls_spider.py`

### sp500 data spider

Once you have the urls you can run the historic data scraper via the following command.

`python3 sp500_data_spider.py`

For running the historic data scraper it may be useful to redirect stdout to some output file

in case of any issues, that way you can continue the scraper from where it left off.

schema:

* company_name

* market_date

* closing_price

* opening_price

* highest_price

* lowest_price

* volume

## tests

run unit tests with `pytest` which will look for the test file beginning with 'test_*'
