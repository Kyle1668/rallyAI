import express from 'express';
import express_graphql from 'express-graphql';
import { buildSchema } from 'graphql';
import dotenv from 'dotenv';
import path from 'path';
import * as tf from '@tensorflow/tfjs-node';
import { MinMaxScaler } from 'machinelearn/preprocessing';

// Enviroment variables
if (process.env.ENV === "dev") {
  dotenv.config();
  console.log("\x1b[35m%s\x1b[0m","Dev Mode, Initializing dotenv library");
}

const knex = require('knex')({
  client: 'pg',
  connection: {
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASS,
    database: process.env.DB_NAME
  }
});

// GraphQL schema
const schema = buildSchema(`
  type Stock {
    id: Int
    symbol: String
    company_name: String
    market_date: String
    closing_price: Float
    opening_price: Float
    highest_price: Float
    lowest_price: Float
    volume_in_millions: String
  }

  type PredictiveStock {
    symbol: String
    predicted_price: Float
    date: String
  }

  type Query {
    statusCode: Int
    error: Boolean
    fromSymbol(stockSymbol: String): [Stock]
    fromDateRange(stockSymbol: String, beginDate: String, endDate: String): [Stock]
    fromPrediction(stockSymbol: String): PredictiveStock
  }
`);

const getDataFromSymbol = async (symbol) => {
  const data = await knex('stocks').where('company_name', symbol);
  if (data.length == 0) {
    throw new Error(`${symbol} isn't apart of S&P 500.`);
  }
  return data;
}

const getFromDateRange = async (symbol, beginDate, endDate) => {
  const data = await knex('stocks')
    .where('symbol', symbol)
    .whereBetween('market_date', [beginDate, endDate]);
  if (data.length == 0) {
    throw new Error(`${symbol} isn't apart of S&P 500.`);
  }
  return data;
}

// Predictive model
const getFromPredictionModel = async (symbol) => {

  // Grabbing data to transform and array manipulations
  const closeData = await knex('stocks').where('company_name', symbol);

  if (closeData.length === 0) {
    throw new Error(`${symbol} isn't apart of S&P 500.`);
  }
  
  const companies = [ "AMD", "Comcast", "Pfizer",
  "Intel",
  "Apple",
  "Micron",
  "Microsoft",
  "Cisco",
  "Facebook",
  "AutoZone"];

  if (!companies.includes(symbol)) {
    throw new Error("Companies model hasn't been trained!");
  }

  const projectDir = path.join(__dirname, '../');
  const model = await tf.loadLayersModel(`file://${projectDir}/stock-predictor/modelBin/${symbol}/model.json`);
  
  const minmaxScaler = new MinMaxScaler({ featureRange: [0,1] });

  // array manipulations for getting 7 day
  const closeDataSortedDates = (closeData.sort((a,b)=> new Date(b.market_date) - new Date(a.market_date))).slice(0,7);

  console.log(closeDataSortedDates);

  const closeDataPriceOnly = closeDataSortedDates.map(v => v.closing_price).reverse();

  const closePrice = await knex.select('closing_price').from('stocks').where('company_name', symbol);

  let closePriceV = closePrice.map(v => v.closing_price);

  minmaxScaler.fit(closePriceV);

  const result = minmaxScaler.transform([[closeDataPriceOnly[0]], [closeDataPriceOnly[1]], [closeDataPriceOnly[2]], [closeDataPriceOnly[3]], [closeDataPriceOnly[4]], [closeDataPriceOnly[5]], [closeDataPriceOnly[6]]]);

  const tensor = tf.tensor3d([result]);

  const prediction = model.predict(tensor);

  const predictedVal = minmaxScaler.inverse_transform(Object.values(prediction.dataSync()));

  return { 'predicted_price': predictedVal[0].toFixed(2), 'company_name': symbol }
}

// Root resolver
const root = {
  fromSymbol: async ({stockSymbol}) => {
    const returnedData = await getDataFromSymbol(stockSymbol);
    return returnedData;
  },
  fromDateRange: async ({stockSymbol, beginDate, endDate}) => {
    const returnedData = await getFromDateRange(stockSymbol,beginDate, endDate);
    return returnedData;
  },
  fromPrediction: async ({stockSymbol}) => {
    const returnedData = await getFromPredictionModel(stockSymbol);
    return returnedData;
  }
};

// Create an express server and a GraphQL endpoint
const app = express();
app.use(
  "/graphql",
  express_graphql({
    schema: schema,
    rootValue: root,
    graphiql: true
  })
);

const serverPort = process.env.PORT || 3000;

app.listen(serverPort, () => console.log("\x1b[5m\x1b[35m%s\x1b[0m",`Express GraphQL Server Now Running On localhost:${serverPort}/graphql`));