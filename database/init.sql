CREATE TABLE stocks
(
    company_name VARCHAR (20) NOT NULL,
    market_date DATE NOT NULL,
    closing_price REAL NOT NULL,
    opening_price REAL,
    highest_price REAL,
    lowest_price REAL,
    volume_in_millions VARCHAR(10),
    percent_change VARCHAR(10)
);