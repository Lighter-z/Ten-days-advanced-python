
/***************
 * Aggregation * 
 ***************/
select count(*) as total_no from sales;

-- Find minimum msrp of all products
select min(msrp) from product;

-- Find maximum msrp of all products
select max(msrp) from product;

select msrp from product order by msrp desc limit 1;

-- Top 2 MSRP of all products;
select name,msrp 
from product
order by msrp desc
limit 2;

-- Find average msrp of all products
select avg(msrp) from product;

-- Find how many kind of products we have

-- Find total of msrp of all kind of products
select AVG(msrp), class 
from product
group by class;


-- Find total sales revenue(amount);
select  sum(price*quantity) as sales_amount 
from sales;



/***************
 *  Group by   * 
 ***************/
-- total sales revenue(amount);
/* format to $xxx.xx*/
SELECT concat('$ ',format(sum(amount),2)) as d_amount FROM fitbit_new.sales_amount;



-- Find total sales revenue by product. Order by sales_amount desendingly;
SELECT sum(amount) as d_amount, product_id
FROM fitbit_new.sales_amount
group by product_id
order by d_amount desc;


-- total # of transactions by product



-- practice: calculate total sales amount, # of transactons, min amount, max amount, 
-- avg amount, total units by product name. Order by total_amounts desendingly;
CREATE OR REPLACE VIEW product_sales as
select 
    p.name,
	sum(amount) total_amount,
    count(s.tran_id) cnt_tran,
    min(amount) min_amount,
    max(amount) max_amount,
    sum(s.quantity) total_unints
from sales_amount s , product p
where s.product_id = p.product_id
group by p.name
order by total_amount desc; -- reporting


-- average price vs weighted(total) average price;



-- count distinct product and client that have sales;
select count(distinct product_id) dist_product, sales.client_id,
       count(*) total
from sales
group by client_id
;

-- how many different/unique products each client purchased;
select c.name, count(distinct s.product_id) dist_product, c.client_id
from sales s, client c
where s.client_id = c.client_id
group by s.client_id
HAVING dist_product > 2
;


-- find clients that purchase more than 1 unique products;


-- practice: find products that are sold less than 20 units;



-- practice: total sales by weekday. hint: use WEEKDAY function to get weekday;





