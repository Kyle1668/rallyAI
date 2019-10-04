CREATE TABLE stocks
(
    symbol VARCHAR (10) PRIMARY KEY,
    company_name VARCHAR (50),
    market_date DATE,
    closing_price REAL,
    opening_price REAL,
    highest_price REAL,
    lowest_price REAL,
    volume_in_millions REAL
);