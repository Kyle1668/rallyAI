FROM node:alpine

LABEL name="RallyAI Stocks Data API"
LABEL version="1.0.0"

WORKDIR /ralliai-api

COPY ./ ./

RUN npm install

EXPOSE 3000

CMD [ "node", "index.js" ]