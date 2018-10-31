/*********************
 *   Date Function   *
 *********************/
 
-- Get current date 
select curdate();

-- Get current timestamp
select current_time(); 

-- Get current timestamp
select current_timestamp(); 

SELECT EXTRACT(month FROM '2009-07-02') as `mon`;

-- Extract specific day/month/year of dates
select extract(day from curdate()) as day_now;
select day(curdate()) as day_now;


select extract(month from curdate()) as month_now;
select month(curdate()) as month_now;

select extract(year from curdate()) as year_now;
select year(curdate()) as year_now;

-- Adddate
select adddate(curdate(),interval 10 day);
select adddate('2017-01-01',interval 10 day);
select adddate('2017-01-01',interval 1 month);
select adddate('2017-01-01',interval 5 year);

SELECT ADDDATE('2008-01-02',100);
SELECT ADDDATE('2008-01-02', INTERVAL 31 DAY);

-- Addtime
select addtime(current_timestamp(),'01:00:00');


-- Datediff
use fitbit_new;

SELECT DATEDIFF('2007-12-31 00:00:00','2007-12-30 23:59:59');
SELECT DATEDIFF('2010-11-30 23:59:59','2010-12-31');

select tran_id,status, arrive_date, eta, 
datediff(arrive_date,eta) as diff_eta
from shipping;

-- Get first day of this month
select adddate(curdate(), interval -day(curdate()-1) day) as first_day;


/*********************
 *  String Function  *
 *********************/

select *
from product;

-- Concat
select concat('String1','String2');
select concat('String1',' ','String2');

select code, name, concat(code,name) as code_name
from product;

-- random()
select RAND();
-- Concat with random number
select code, name, concat(code,RAND()) as code_name
from product;

-- Left
select code, name, left(name,2)
from product;

-- right
select code, name, right(name,2)
from product;

-- Substring
select code, class, substring(class,2,6)
from product;

select code, class, substring(class,4,6)
from product;

-- lower case
select code, class, lower(class)
from product;

-- upper case
select code, name, upper(name)
from product;

-- Length
select code, name, length(name)
from product;

select name, class, concat(upper(left(class,1)), lower(substring(class,2,length(class))))
from product;

-- Trim
select '     Mytext    ';
select length( '     Mytext    ');

select ltrim( '     Mytext    '),length(ltrim( '     Mytext    ')) as len;
select rtrim( '     Mytext    '),length(rtrim( '     Mytext    ')) as len;

select ltrim(rtrim( '     Mytext    '));
select length(ltrim(rtrim( '     Mytext    ')));



