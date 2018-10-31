/***************
 * Sub Query   * 
 ***************/
SELECT * FROM sales WHERE product_id = 1;


SELECT * FROM sales 
WHERE product_id = (SELECT product_id FROM product limit 1);
 
 
-- find all transactions that have shipping info;
select s.*
from sales s
inner join shipping sh
on s.tran_id = sh.tran_id;

select *
from sales 
where tran_id in (select tran_id from shipping);

select *
from sales s
where exists
(select * from shipping sh where s.tran_id = sh.tran_id);


-- find transactions that don't exist in shipping table;
select s.*
from sales s
left join shipping sh
on s.tran_id = sh.tran_id
where sh.tran_id is NULL;

select s.*
from sales  s
where tran_id not in (select tran_id from shipping);

select *
from sales s
where not exists
(select * from shipping sh where s.tran_id = sh.tran_id);

-- find clients that have no sales;
-- insert client

-- find sales that happened after any of the transactions have arrived;
select * from sales
where date > any (select arrive_date from shipping);

select * from sales
where date > (select min(arrive_date) from shipping);

-- find transactions that happened after all shipping arrived date;
SELECT 
    *
FROM
    sales
WHERE
    date > ALL (SELECT 
            arrive_date
        FROM
            shipping
        WHERE
            arrive_date IS NOT NULL);


SELECT 
    *
FROM
    sales
WHERE
    date > (SELECT 
            MAX(arrive_date)
        FROM
            shipping
        WHERE
            arrive_date IS NOT NULL);


/***********************
 *     case when       *
 ***********************/
-- calculate total online sales and offline sales;
select type, sum(amount) as total_amt
from sales_amount s, client c
where s.client_id = c.client_id
group by c.type;


-- show online and offline in seperate columns;
select  
sum( case temp.type when 'OFFLINE' then total_amt 
	 WHEN 'ONLINE' then 0 end ) as offline, 
sum(case when temp.type = 'ONLINE' then total_amt 
	 else 0 end ) as online
from 
(select type, sum(amount) as total_amt
from sales_amount s, client c
where s.client_id = c.client_id
group by c.type) temp;

-- practice: show above table by product 
-- (for each product, show total online sales and total offline sales);
CREATE OR REPLACE VIEW product_sales_channel as
select  p.name,
sum( case temp.type when 'OFFLINE' then total_amt 
	 WHEN 'ONLINE' then 0 end ) as offline, 
sum(case when temp.type = 'ONLINE' then total_amt 
	 else 0 end ) as online
from 
(select type, sum(amount) as total_amt, s.product_id
from sales_amount s, client c
where s.client_id = c.client_id
group by c.type, s.product_id) temp
inner join product p 
on p.product_id = temp.product_id
group by 1
;


/**************  explain  *******************/
SELECT @@profiling;
SET profiling = 0;

select * 
from sales s 
inner join shipping sh
on s.tran_id = sh.tran_id
;

select * 
from sales s
where  exists
(select * from shipping sh 
where s.tran_id = sh.tran_id); 
