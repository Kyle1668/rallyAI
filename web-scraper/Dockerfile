FROM joyzoursky/python-chromedriver:3.6-alpine3.7-selenium

WORKDIR /usr/src/rallyAI/web-scraper
COPY . /usr/src/rallyAI/web-scraper

ENV PATH="${PATH};/usr/src/rallyAI/web-scraper/drivers"

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

RUN pip3 install -r requirements.txt

CMD ["python3", "commodities_scrapers.py"]