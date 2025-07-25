/* -----------DAY1--------
1.The inventory team wants to identify products that haven't been sold. 
Create a view listing all products that have zero sales.*/

CREATE VIEW vw_UnsoldProducts AS
SELECT p.product_id, p.product_name, p.list_price
FROM production.products p
LEFT JOIN sales.order_items oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL;

/*2. Write a query that:
Ranks products within each category by list price (highest first)
Returns only the first product per category
*/

SELECT * FROM 
(SELECT product_id,product_name,category_id,list_price,
RANK() OVER (PARTITION BY category_id ORDER BY list_price DESC) AS rnk
FROM production.products
) ranked_products
WHERE rnk = 1;


/*--------DAY2--------------
1.Write a scalar-valued function that takes a product_id as input and returns the list_price of that product.
*/

CREATE FUNCTION fn_GetListPrice (@product_id INT)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @list_price DECIMAL(10,2)
    SELECT @list_price = list_price
    FROM production.products
    WHERE product_id = @product_id

    RETURN @list_price
END
SELECT dbo.fn_GetListPrice(101) AS ListPrice;

/*2.Write an inline table-valued function that returns all products for a given category_id.*/
CREATE FUNCTION fn_GetProductsByCategory (@category_id INT)
RETURNS TABLE
AS
RETURN (
    SELECT product_id, product_name, list_price
    FROM production.products
    WHERE category_id = @category_id
);

SELECT * FROM dbo.fn_GetProductsByCategory(2);

-- 3.Create a function that takes a store_id and returns the total sales amount for that store.
-- Use the sales.orders and sales.order_items tables. 
-- Sum the list_price * quantity for all orders from that store.

CREATE FUNCTION fn_TotalSalesByStore (@store_id INT)
RETURNS DECIMAL(18,2)
AS
BEGIN
    DECLARE @total_sales DECIMAL(18,2)
    SELECT @total_sales = SUM(oi.list_price * oi.quantity)
    FROM sales.orders o
    JOIN sales.order_items oi ON o.order_id = oi.order_id
    WHERE o.store_id = @store_id

    RETURN ISNULL(@total_sales, 0)
END
SELECT dbo.fn_TotalSalesByStore(3) AS TotalSales;

--4.Write a table-valued function that takes two dates as input and returns all orders placed between those dates.
CREATE FUNCTION fn_GetOrdersBetweenDates (@start_date DATE, @end_date DATE)
RETURNS TABLE
AS
RETURN (
    SELECT order_id, customer_id, order_date, store_id
    FROM sales.orders
    WHERE order_date BETWEEN @start_date AND @end_date
);
SELECT * FROM dbo.fn_GetOrdersBetweenDates('2016-01-01', '2016-12-31');

--5.Write a function that takes a brand_id and returns the number of products for that brand.

CREATE FUNCTION fn_CountProductsByBrand (@brand_id INT)
RETURNS INT
AS
BEGIN
    DECLARE @product_count INT
    SELECT @product_count = COUNT(*)
    FROM production.products
    WHERE brand_id = @brand_id

    RETURN @product_count
END
SELECT dbo.fn_CountProductsByBrand(5) AS ProductCount;


/*------------DAY3------------
1. Create a trigger that logs any update to the list_price of a product in the production.products table.
in a new table price_change_log
logid
    product_id 
    old_price
    new_price   
  change_date*/

CREATE TABLE price_change_log (
  logid INT IDENTITY(1,1) PRIMARY KEY,
  product_id INT,
  old_price DECIMAL(10,2),
  new_price DECIMAL(10,2),
  change_date DATETIME
)
CREATE TRIGGER tr_products_listprice_update1
ON production.products
FOR UPDATE
AS
BEGIN
    DECLARE @ProductId INT
    DECLARE @OldPrice DECIMAL(10,2), @NewPrice DECIMAL(10,2)

    -- Create temp table to hold new values
    SELECT * 
    INTO #TempProducts 
    FROM inserted

    -- Loop through each updated row
    WHILE EXISTS (SELECT product_id FROM #TempProducts)
    BEGIN
        -- Fetch the first row from temp
        SELECT TOP 1 
            @ProductId = product_id, 
            @NewPrice = list_price 
        FROM #TempProducts

        -- Get old price from deleted table
        SELECT @OldPrice = list_price 
        FROM deleted 
        WHERE product_id = @ProductId

        -- Only log if price actually changed
        IF (@OldPrice <> @NewPrice)
        BEGIN
            INSERT INTO price_change_log (product_id, old_price, new_price, change_date)
            VALUES (@ProductId, @OldPrice, @NewPrice, GETDATE())
        END

        -- Remove the row we just processed
        DELETE FROM #TempProducts WHERE product_id = @ProductId
    END
END

select * from production.products
SELECT * FROM price_change_log
UPDATE production.products
SET list_price = 750.00
WHERE product_id = 101

--2. Create a trigger that Prevent deletion of a product if it exists in any open order.

CREATE TRIGGER tr_prevent_product_delete_if_in_open_order
ON production.products
FOR DELETE
AS
BEGIN
    -- Prevent deletion of products that are in any OPEN order (status < 4)
    IF EXISTS (
        SELECT 1
        FROM deleted d
        JOIN sales.order_items oi ON d.product_id = oi.product_id
        JOIN sales.orders o ON oi.order_id = o.order_id
        WHERE o.order_status < 4
    )
    BEGIN
        RAISERROR ('Cannot delete product. It exists in an open order.', 16, 1)
        ROLLBACK TRANSACTION
    END
END


DELETE FROM production.products WHERE product_id = 1;


/* BASIC SQL Assignments
1) Total Sales by Store (Only High-Performing Stores)
List each store's name and the total sales amount (sum of quantity × list price) for all orders. 
Only include stores where the total sales amount exceeds $50,000.*/


SELECT s.store_name,
SUM(oi.quantity * oi.list_price) AS total_sales
FROM sales.orders o
JOIN sales.order_items oi ON o.order_id = oi.order_id
JOIN sales.stores s ON o.store_id = s.store_id
GROUP BY s.store_name
HAVING SUM(oi.quantity * oi.list_price) > 50000;

/*2) Top Selling Products by Quantity 
Find the top 5 best-selling products by total quantity ordered.
*/
SELECT p.product_name,
SUM(oi.quantity) AS total_quantity
FROM production.products p
JOIN sales.order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_name
ORDER BY total_quantity DESC
OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY;

--3) how monthly sales totals (sum of line total) for the year 2016.
SELECT FORMAT(o.order_date, 'yyyy-MM') AS month,
SUM(oi.quantity * oi.list_price) AS monthly_sales
FROM sales.orders o
JOIN sales.order_items oi ON o.order_id = oi.order_id
WHERE YEAR(o.order_date) = 2016
GROUP BY FORMAT(o.order_date, 'yyyy-MM')
ORDER BY month;

---4) High Revenue Stores List all stores whose total revenue is greater than ?100,000
SELECT s.store_name,
SUM(oi.quantity * oi.list_price) AS total_revenue
FROM sales.orders o
JOIN sales.order_items oi ON o.order_id = oi.order_id
JOIN sales.stores s ON o.store_id = s.store_id
GROUP BY s.store_name
HAVING SUM(oi.quantity * oi.list_price) > 100000;

