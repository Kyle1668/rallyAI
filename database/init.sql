CREATE TABLE stocks
(
    symbol VARCHAR (10) PRIMARY KEY,
    company_name VARCHAR (50) NOT NULL,
    market_date DATE NOT NULL,
    closing_price REAL NOT NULL,
    opening_price REAL,
    highest_price REAL,
    lowest_price REAL,
    volume_in_millions REAL
);