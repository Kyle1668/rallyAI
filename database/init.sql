CREATE TABLE stocks
(
    company_name VARCHAR (10) PRIMARY KEY,
    market_date VARCHAR (20) NOT NULL,
    closing_price REAL NOT NULL,
    opening_price REAL,
    highest_price REAL,
    lowest_price REAL,
    volume_in_millions REAL,
    percent_change VARCHAR(10)
);