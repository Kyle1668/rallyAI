# rallyAI: GraphQL API for Predictive Stock Analytics

## Summary

rallyAI is an open-source GraphQL web API for stock data. Clients are able to query for historical and current stock data including price, volume, etc. In developing this project, our team will be exposed to the full machine learning engineering lifecycle from data set creation, model training, API development, and automated cloud deployments.

## Technical Overview

We'll first gather data by web scraping online stock data websites such as investing.com. At first, we’ll only focus on the 500 large company stocks comprising the S&P 500 index.

Once our scraper has been developed, on a daily basis we’ll scrape historical stock data output the raw data as a CSV.

Once all the data has been gathered, we’ll develop a supervised machine learning model to predict stock prices. We need to decide on whether we wish to predict the closing price for a stock when the market is in session or to predict the stock for the next day.

With our model trained, we’ll export the weights and model architecture to the language of our API. From there we'll develop an API that taken in the index of stock in the S&P 500 and returns its data and prediction.

Once the API is completed, we’ll add authentication, API key registration, and deploy it with Docker and Kubernetes.

## Technologies:

**Web Scraping**: Python, Beautiful Soup, Selenium, Docker

**ETL**: Spark

**Machine Learning**: Keras

**API**: Typescript, GraphQL, KerasJS

**Deployment**: Docker, Kubernetes, Terraform

## Components

### Database

#### info

`database` contains the file for initialzing database with schema

### API
=======
# API Usage

## Query Syntax and Types

For our public API application, there are many different queries to call from and there associated data values. The most basic type in this API will be the `Stock` and is described by:

```graphql
  type Stock {
    id: Int
    company_name: String
    market_date: String
    closing_price: Float
    opening_price: Float
    highest_price: Float
    lowest_price: Float
    volume_in_millions: String
  }
```

Another important type will be `PredictiveStock`

```graphql
  type PredictiveStock {
    company_name: String
    predicted_price: Float
  }
```

## Writing Queries
There are 3 queries that are currently available in our API.

1. `fromSymbol(stockSymbol: String): [Stock]`
2. `fromDateRange(stockSymbol: String, beginDate: String, endDate: String): [Stock]`
3. `fromPrediction(stockSymbol: String): PredictiveStock`


```graphql
{
    fromSymbol(stockSymbol: "Microsoft") {
        company_name
        market_date
        closing_price
        opening_price
        highest_price
        lowest_price
        volume_in_millions
    }
}
```

`fromSymbol()` above query will produce the following JSON response (an array of Microsoft stock information), given the stockSymbol "Microsoft".

```json
{
    "data": {
    "fromSymbol": [
      {
        "company_name": "Microsoft",
        "market_date": "Jul 15, 2013",
        "closing_price": 36.17,
        "opening_price": 35.66,
        "highest_price": 36.22,
        "lowest_price": 35.58,
        "volume_in_millions": null
      },
      {
        "company_name": "Microsoft",
        "market_date": "Nov 11, 2019",
        "closing_price": 146.11,
        "opening_price": 145.34,
        "highest_price": 146.42,
        "lowest_price": 144.73,
        "volume_in_millions": null
      },
      {
        "company_name": "Microsoft",
        "market_date": "Nov 08, 2019",
        "closing_price": 145.96,
        "opening_price": 143.98,
        "highest_price": 145.99,
        "lowest_price": 143.76,
        "volume_in_millions": null
      },
      ...
      ...
    }]
}
```

```graphql
{
  fromDateRange(stockSymbol: "Microsoft", beginDate: "Jul 28, 2019", endDate: "Jul 30, 2019") {
        company_name
        market_date
        closing_price
        opening_price
        highest_price
        lowest_price
        volume_in_millions
  }
}
```

`fromDateRange()` above query will produce the following JSON response (an array of Microsoft stocks between some user specified dates (July 28th to 30th 2019)).

```json
{
  "data": {
    "fromDateRange": [
      {
        "company_name": "Microsoft",
        "market_date": "Jul 30, 2019",
        "closing_price": 140.35,
        "opening_price": 140.14,
        "highest_price": 141.22,
        "lowest_price": 139.8,
        "volume_in_millions": null
      },
      {
        "company_name": "Microsoft",
        "market_date": "Jul 29, 2019",
        "closing_price": 141.03,
        "opening_price": 141.5,
        "highest_price": 141.51,
        "lowest_price": 139.37,
        "volume_in_millions": null
      },
      ...
      ...
    ]
  }
}
```

```graphql
{
    fromPrediction(stockSymbol: "Microsoft") {
        company_name
        predicted_price
    }
}
```

`fromPrediction()` above query will produce a price prediction based off of previous stock data for Microsoft and will produce the following JSON response.

```json
{
  "data": {
    "fromPrediction": {
      "company_name": "Microsoft",
      "predicted_price": 140.68
    }
  }
}
```

### Stock Predictor

#### info

stock-predictor contains one script that exports company stock predictor model: `train.py`
`train.py` retrieves data from a Postgre database, trains a model based on specified
company and exports the model using tensorflowJS-converter.

#### dependencies and installation

Python : version = 3.6

`python3 -m pip install --user virtualenv`

`python3 -m venv env`

`pip3 install -r requirements.txt`

#### usage

##### train

Run script below to export a model for a specified company name

`python3.6 train.py [company name]`

### web-scraper

#### info

web-scraper contains two web scraping 'crawlers': `sp500_data_spider.py` and `sp500_urls_spider.py`

`sp500_urls_spider.py` retrieves the urls for each of the sp500 comapnies from investing.com and writes

the result to a json object containing the company name as a key and the url as it's value. This json

is then saved to a file named 'urls/sp500_urls.json'.


The `sp500_data_spider.py` grabs the file containing the urls to scrape historic data for each of the

companies contained in the 'urls/sp500_urls.json' file. The scraper loads a historic data table for

each company and collects data over a time span of ten years ago from the current date. All this data

gets saved to one large .csv file under 'data/sp500data.csv'.


#### dependencies and installation

Python : version = 3.7.4

`python3 -m pip install --user virtualenv`

`python3 -m venv env`

`pip3 install -r requirements.txt`

You must also install the latest **chromedriver** and save the location of the driver to your `$PATH`

#### usage

##### sp500 urls spider

Run the urls spider using python3 and redirect the output to either a .json or .jl file

`python3 sp500_urls_spider.py`

##### sp500 data spider

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

#### tests

run unit tests with `pytest` which will look for the test file beginning with 'test_*'


