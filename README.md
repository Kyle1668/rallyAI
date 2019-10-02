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
