create database transactions;
use transactions;

CREATE TABLE finance_info(
	id int NOT NULL AUTO_INCREMENT,
	ticker varchar(6),
    price varchar(10),
    transaction_date date,
    transaction_type varchar(4),
    quantity int,
    account_number varchar(15),
    create_date dateTime,
    PRIMARY KEY (id)
	);
DROP TABLE finance_info;
SELECT * from finance_info;
SELECT * FROM finance_info ORDER BY quantity DESC LIMIT 20;
delete from finance_info;

SHOW GLOBAL VARIABLES LIKE 'local_infile';
SET GLOBAL local_infile = true;

LOAD DATA LOCAL INFILE 'C:/Projects/financeSite/FINANCE_DATA.csv'
INTO TABLE finance_info
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(ticker,price,transaction_date,transaction_type,quantity,account_number,create_date)
SET ID = NULL;



CREATE TABLE top_vals (
	id INT,
    multiplied DEC (40,20)
);
DROP TABLE top_vals;

SELECT * FROM top_vals;
SELECT COUNT(*) FROM top_vals;
DELETE FROM top_vals;

INSERT INTO top_vals
VALUES (4, 5.22);