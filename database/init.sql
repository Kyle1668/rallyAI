CREATE TABLE stocks
(
<<<<<<< HEAD
    company_name VARCHAR (10) PRIMARY KEY,
    market_date VARCHAR (20) NOT NULL,
=======
    company_name VARCHAR (20) NOT NULL,
    market_date DATE NOT NULL,
>>>>>>> b92b5e8610b9ea3d10d19e523d28fdd830819edb
    closing_price REAL NOT NULL,
    opening_price REAL,
    highest_price REAL,
    lowest_price REAL,
<<<<<<< HEAD
    volume_in_millions REAL,
=======
    volume_in_millions VARCHAR(10),
>>>>>>> b92b5e8610b9ea3d10d19e523d28fdd830819edb
    percent_change VARCHAR(10)
);