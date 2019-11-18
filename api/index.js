import express from 'express';
import express_graphql from 'express-graphql';
import {
  buildSchema
} from 'graphql';

// Enviroment variables
import dotenv from 'dotenv';
dotenv.config();

var knex = require('knex')({
  client: 'pg',
  connection: {
    host : '127.0.0.1',
    user : 'joseph',
    password : 'password',
    database : 'rallyai'
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

  type Query {
    statusCode: Int
    error: Boolean
    results(stockSymbol: String): [Stock]
  }
`);

const getDataFromSymbol = async (symbol) => {
  const data = await knex('stocks').where('symbol', symbol);
  return data;
}

// Root resolver
const root = {
  results: async ({stockSymbol}) => {
    const returnedData = await getDataFromSymbol(stockSymbol);
    console.log(returnedData);
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

app.listen(3000, () =>
  console.log(`Express GraphQL Server Now Running On localhost:${serverPort}/graphql`)
);