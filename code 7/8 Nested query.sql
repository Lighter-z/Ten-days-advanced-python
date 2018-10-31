/*****************
 * Nested Query  *
 *****************/

-- group total sales amount by product name, shipping status
SELECT 
    p.product_id, p.name, (
    case when  temp.status  is NULL then 'NOT SHIP YET!' 
    else temp.status end) new_status
    , tamount
FROM
    (SELECT 
        product_id, status, SUM(quantity * price) AS tamount
    FROM
        sales s
	left join shipping sh
    on s.tran_id = sh.tran_id
    GROUP BY 1 , 2) temp
        INNER JOIN
    product p ON p.product_id = temp.product_id;

-- percent of sales by weeday;

select wk_day + 1, concat(round((wk_amt / total_amt)*100), '%') as wk_pct
from
(select weekday(date) as wk_day, sum(amount) as wk_amt
from sales_amount
group by 1) t1,
(select sum(amount) as total_amt from sales_amount) t2
;

-- percent of customers that ever purchased;
select
concat(round(count(distinct c.client_id)
/ (select count(distinct client_id) from client) * 100),'%') 
as client_pct
from client c, sales s
where c.client_id = s.client_id



