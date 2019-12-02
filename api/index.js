import express from 'express';
import express_graphql from 'express-graphql';
import { buildSchema } from 'graphql';
import dotenv from 'dotenv';
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
    fromPrediction(stockSymbol: String, closingPrice: Float): PredictiveStock
  }
`);

const getDataFromSymbol = async (symbol) => {
  const data = await knex('stocks').where('company_name', symbol);
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

  const model = await tf.loadLayersModel("file:///Users/joseph/Desktop/School/cse115a/rallyAI/stock-predictor/modelBin/AutoZone/model.json");
  
  const minmaxScaler = new MinMaxScaler({ featureRange: [0,1] });

  // Official Function for Database
  // const closeData = await knex.select('closing_price').from('stocks').where('company_name', symbol);

  // Mock function
  const closeDataMock = await knex.select('closing_price').from('stocks').where('company_name', 'AutoZone');

  let closeDataV = closeDataMock.map(v => v.closing_price);

  minmaxScaler.fit(closeDataV);

  // FIX THIS
  const result = minmaxScaler.transform([[980.98], [982.56], [989.8], [978.36], [981.34], [984.09], [977.83]]);

  const tensor = tf.tensor3d([result]);

  const prediction = model.predict(tensor);

  const predictedVal = minmaxScaler.inverse_transform(Object.values(prediction.dataSync()));

  return { 'predicted_price': predictedVal[0].toFixed(2) }
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
  fromPrediction: async ({stockSymbol, closingPrice}) => {
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