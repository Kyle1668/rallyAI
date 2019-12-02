CREATE TABLE stocks
(
    company_name VARCHAR (20) NOT NULL,
    market_date VARCHAR (20) NOT NULL,
    closing_price FLOAT NOT NULL,
    opening_price FLOAT,
    highest_price FLOAT,
    lowest_price FLOAT,
    volume_in_millions VARCHAR(10),
    percent_change VARCHAR(10)
);