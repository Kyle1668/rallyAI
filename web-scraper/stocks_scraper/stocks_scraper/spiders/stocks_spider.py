import scrapy

# treat this as an example for now, it's mostly for demonstration


class StocksSpider(scrapy.Spider):
    name = "stocks"

    # useful if we're reading from several pages
    start_urls = [
        'https://money.cnn.com/data/hotstocks/index.html',
    ]

    def parse(self, response):
        headers = ['company', 'price', 'change', 'delta']
        mostActives = response.css("table.wsod_dataTable")[0]
        i = 0
        for stock in mostActives.css("td"):
            yield {
                headers[i]: stock.css("span::text").get()
            }
            i = i + 1 if i != 3 else 0
