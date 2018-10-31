
/*************************************** 
 *        DDL: Create Database         * 
 ***************************************/

-- drop existing database if exists;
DROP DATABASE IF EXISTS fitbit_new;

-- create database;
CREATE DATABASE fitbit_new;

-- use database;
USE fitbit_new;


/*************************************** 
 *           DDL: Create Table         * 
 ***************************************/

/*        product          */
-- create table product;
DROP TABLE IF EXISTS product, client, sales;

CREATE TABLE IF NOT EXISTS product (
    product_id INT NOT NULL,
    code CHAR(5) NOT NULL,
    name VARCHAR(20) NOT NULL,
    class VARCHAR(45) NOT NULL,
    color VARCHAR(45) NOT NULL,
    has_clock ENUM('Y', 'N') NOT NULL,
    msrp DECIMAL(9 , 2 ) NULL,
    PRIMARY KEY (product_id),
    UNIQUE KEY (code),
    INDEX product_id_idx (product_id)
);

describe product;

-- create index seprately
CREATE UNIQUE INDEX name_idx on product(name);
DROP INDEX name_idx ON product;

-- alter table;
ALTER TABLE product ADD COLUMN description VARCHAR(100) NOT NULL after name;

ALTER TABLE product CHANGE COLUMN description `desc` VARCHAR(200) NOT NULL;
describe product;

ALTER TABLE product DROP COLUMN `desc`;


/*       client      */
-- create table client;
CREATE TABLE IF NOT EXISTS client (
    client_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,  -- user name, email
    type VARCHAR(45) NULL,
    PRIMARY KEY (client_id),
    UNIQUE KEY (name)
);

describe client;

/*        sales         */
-- create table sales;
CREATE TABLE IF NOT EXISTS sales (
    tran_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    date DATE NOT NULL,
    product_id INT NOT NULL,
    client_id INT NOT NULL,
    price DECIMAL(9 , 2 ) NOT NULL,
    quantity INT NULL DEFAULT 1,
    PRIMARY KEY (`tran_id`),
	INDEX   fk_client_id_idx (client_id ASC),
    CONSTRAINT fk_product_id FOREIGN KEY (product_id)
        REFERENCES product (product_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_client_id FOREIGN KEY (client_id)
        REFERENCES client (client_id)
        ON DELETE CASCADE,
    CONSTRAINT chek_price CHECK (price > 0)
);

show tables;

-- create foreign key seperately;
-- drop foreign key;


-- add update cascade;
ALTER TABLE sales DROP FOREIGN KEY fk_product_id;
ALTER TABLE sales DROP FOREIGN KEY fk_client_id;

ALTER TABLE sales ADD CONSTRAINT fk_product_id 
        FOREIGN KEY (product_id)
        REFERENCES product (product_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE;
        
ALTER TABLE sales ADD CONSTRAINT fk_client_id 
        FOREIGN KEY (client_id)
        REFERENCES client (client_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE; 

-- create view;
CREATE OR REPLACE VIEW sales_amount as 
	SELECT *, price*quantity as amount
    FROM sales;

  
/********************************************** 
 *        DML: Insert, Update, Delete         * 
 **********************************************/
describe product;

INSERT INTO product 
VALUES
(1,'E-ZIP','Zip','EVERYDAY','GREEN','Y',59.95),
(2,'E-FLX','Flex','EVERYDAY','BLACK','N',99.95),
(3,'A-BLZ','Blaze','ACTIVE','PURPLE','Y',199.95),
(4,'P-SUG','Surge','PERFORMANCE','BLACK','Y',249.95);

-- update product;
UPDATE product 
SET 
    product_id = 10
WHERE
    product_id = 1;

SELECT * from product;

-- cascade delete
DELETE FROM product 
WHERE product_id = 10;

INSERT INTO product 
VALUES
(1,'E-ZIP','Zip','EVERYDAY','GREEN','Y',59.95);


INSERT INTO client 
VALUES
(1,'FITBIT','ONLINE'),
(2,'AMAZON','ONLINE'),
(3,'BESTBUY','OFFLINE'),
(4,'WALMART','OFFLINE')
;
-- if client and product is ready, we can not insert sales records
INSERT INTO sales 
(tran_id, date, product_id, client_id, price, quantity)
VALUES
(1,'2016-6-1', 1, 1, 40, 10),
(2,'2016-6-5', 1, 2, 30, 5),
(3,'2016-6-8', 2, 1, 80, 8),
(4,'2016-6-8', 2, 2, 70, 7),
(5,'2016-6-13', 3, 2, 150, 5),
(6,'2016-6-18', 3, 4, 150, 10),
(7,'2016-6-20', 2, 4, 40, 15);

-- update sales;
UPDATE sales 
SET `date` ='2016-6-21', price=200
WHERE `date` ='2016-6-20' and tran_id = 7;

select * from sales where tran_id = 7;

-- create table SHIPPING;
DROP TABLE IF EXISTS shipping;

CREATE TABLE IF NOT EXISTS shipping (
    shipping_id INT NOT NULL auto_increment,
    tran_id INT NOT NULL,
    tracking_no INT,
    status ENUM('PREPARING', 'SHIPPED', 'ARRIVED') default 'PREPARING',
    arrive_date DATE,
    eta DATE,
    PRIMARY KEY (shipping_id)
);

INSERT INTO shipping
(tran_id,tracking_no,status,arrive_date,eta)
VALUES
 (3, 103, 'ARRIVED', '2016-06-02', '2016-06-02'),
 (4, 104, 'ARRIVED', '2016-06-30', '2016-06-25'),
 (5, 105, 'SHIPPED', NULL,         '2016-03-04'),
 (20, 200, 'PREPARING', NULL, NULL);

 