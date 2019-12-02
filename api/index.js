import express from 'express';
import express_graphql from 'express-graphql';
import { buildSchema } from 'graphql';
import dotenv from 'dotenv';
import * as tf from '@tensorflow/tfjs';

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
    fromPrediction(stockSymbol: String, closingPrice: Float): PredictiveStock
  }
`);

const getDataFromSymbol = async (symbol) => {
  const data = await knex('stocks').where('symbol', symbol);
  return data;
}

const getFromDateRange = async (symbol, beginDate, endDate) => {
  const data = await knex('stocks')
    .where('symbol', symbol)
    .whereBetween('market_date', [beginDate, endDate]);
  return data;
}

// Predictive model
const getFromPredictionModel = async (symbol, closingPrice) => {

  // const prediction = // call the model
  const model = await tf.loadLayersModel(`./stock-predictor/modelBin/${symbol}/model.json`);

   // return prediction
  return model.predict(closingPrice);
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
    const returnedData = await getFromPredictionModel(stockSymbol, closingPrice);
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