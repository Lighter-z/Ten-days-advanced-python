
/***************
 * join tables *
 ***************/
 
-- list all sales for FLEX and BLAZE;

-- what happens without a.product_id=b.product_id;
-- use table alias;

 
 
-- practice: list all transactions with Amazon;



-- practice: list sales date, client_name, sales_amount for FLEX;



-- list all sales with msrp > 100 and quantity >= 10, or quality >= 100; ignore non-existing product_id in PRODUCT;
-- ignore non-existing product_id in PRODUCT;



/***************
*     Join     * 
***************/

-- list all transactions; show shipping status if there is any;



-- show all transactions with shipping status;

/* inner join */


-- list all shipments with shipping status; show client_id and product_id if exists;
-- list all shipping status with client_id and product_id;
/* right join */


-- list all sales and shipping status in one table;


-- list all transactions and shipping status in one table;
/* full join */

; -- MySQL doesn't support full join!


/*********************
 *    set operators  *
 *********************/
-- union;


-- union all


-- intersect



-- except


