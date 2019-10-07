# WEB-SCRAPER

## info

boilerplate for the webscraper we'll be using to gather data on market trends

stocks_spider.py is only being shown as an example right now

## dependencies

Python : version = 3.7.4

`pip3 install -r requirements.txt`

## commands

Run a spider to crawl a webpage and direct the output to a file

`scrapy crawl <spider-name> -o <output-file>`

Run commands live from scrapy's shell against some url

`scrapy shell <url>`

While the shell is running you can execute scrapy commands like the following

`response.css('title::text').getall()`

`table = response.css('table')[0]`

`row = table.css('tr')[0]`

## demo

`cd web-scraper/stocks_scraper/`

`scrapy crawl stocks -o test-data/stocks.jl`

## notes

Scrapy tutorial straight from their documentation : https://docs.scrapy.org/en/latest/intro/tutorial.html
