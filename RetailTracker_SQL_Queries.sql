-- ============================================================
-- RETAILTRACKER: Retail Demand Intelligence System
-- Author: Simpson Gundlapally
-- Dataset: Retail Sales 2024 (5,200 records)
-- Tool: SQL (compatible with MySQL / PostgreSQL / SQLite)
-- ============================================================

-- ============================================================
-- STEP 1: DATA EXPLORATION
-- ============================================================

-- 1.1 Preview the raw data
SELECT * FROM retail_sales LIMIT 10;

-- 1.2 Count total records
SELECT COUNT(*) AS total_records FROM retail_sales;

-- 1.3 Check date range of data
SELECT 
    MIN(Date) AS earliest_date,
    MAX(Date) AS latest_date
FROM retail_sales
WHERE Date IS NOT NULL AND Date != '';

-- 1.4 Check all product categories
SELECT DISTINCT Category, COUNT(*) AS product_count
FROM retail_sales
GROUP BY Category
ORDER BY product_count DESC;

-- ============================================================
-- STEP 2: DATA CLEANING & VALIDATION
-- ============================================================

-- 2.1 Find records with missing or empty dates
SELECT Transaction_ID, Date, Category, Net_Sales
FROM retail_sales
WHERE Date IS NULL OR Date = '';

-- 2.2 Find records with NULL quantity (data entry issues)
SELECT Transaction_ID, Product_Name, Quantity, Net_Sales
FROM retail_sales
WHERE Quantity IS NULL;

-- 2.3 Find invalid discount values (outside 0-100 range)
SELECT Transaction_ID, Product_Name, Discount_Percent
FROM retail_sales
WHERE Discount_Percent < 0 OR Discount_Percent > 100;

-- 2.4 Find records with NULL or negative Net Sales
SELECT Transaction_ID, Product_Name, Quantity, Net_Sales
FROM retail_sales
WHERE Net_Sales IS NULL OR Net_Sales < 0;

-- 2.5 Count all dirty records
SELECT 
    SUM(CASE WHEN Date IS NULL OR Date = '' THEN 1 ELSE 0 END)          AS missing_dates,
    SUM(CASE WHEN Quantity IS NULL THEN 1 ELSE 0 END)                    AS missing_qty,
    SUM(CASE WHEN Discount_Percent < 0 
             OR Discount_Percent > 100 THEN 1 ELSE 0 END)               AS invalid_discounts,
    SUM(CASE WHEN Net_Sales IS NULL THEN 1 ELSE 0 END)                   AS missing_sales,
    COUNT(*) AS total_rows
FROM retail_sales;

-- 2.6 Create cleaned view (excluding dirty records)
CREATE VIEW retail_clean AS
SELECT *
FROM retail_sales
WHERE 
    Date IS NOT NULL AND Date != ''
    AND Quantity IS NOT NULL
    AND Discount_Percent >= 0 AND Discount_Percent <= 100
    AND Net_Sales IS NOT NULL AND Net_Sales > 0;

-- Verify cleaned dataset
SELECT COUNT(*) AS clean_records FROM retail_clean;

-- ============================================================
-- STEP 3: SALES PERFORMANCE ANALYSIS
-- ============================================================

-- 3.1 Total revenue by category (High Demand Identification)
SELECT 
    Category,
    COUNT(*) AS total_transactions,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(Net_Sales), 2) AS total_revenue,
    ROUND(AVG(Net_Sales), 2) AS avg_order_value,
    ROUND(SUM(Net_Sales) * 100.0 / SUM(SUM(Net_Sales)) OVER (), 2) AS revenue_share_pct
FROM retail_clean
GROUP BY Category
ORDER BY total_revenue DESC;

-- 3.2 Top 10 best-selling products
SELECT 
    Product_Name,
    Category,
    SUM(Quantity) AS total_units_sold,
    ROUND(SUM(Net_Sales), 2) AS total_revenue,
    ROUND(AVG(Unit_Price), 2) AS avg_price
FROM retail_clean
GROUP BY Product_Name, Category
ORDER BY total_units_sold DESC
LIMIT 10;

-- 3.3 Monthly sales trend (for trend line chart)
SELECT 
    SUBSTR(Date, 1, 7) AS month,
    COUNT(*) AS transactions,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(Net_Sales), 2) AS monthly_revenue,
    ROUND(AVG(Net_Sales), 2) AS avg_basket_size
FROM retail_clean
GROUP BY SUBSTR(Date, 1, 7)
ORDER BY month;

-- 3.4 Revenue by city (geographical analysis)
SELECT 
    City,
    Store_Name,
    COUNT(*) AS transactions,
    ROUND(SUM(Net_Sales), 2) AS total_revenue,
    ROUND(AVG(Net_Sales), 2) AS avg_order_value
FROM retail_clean
GROUP BY City, Store_Name
ORDER BY total_revenue DESC;

-- ============================================================
-- STEP 4: CUSTOMER BEHAVIOUR ANALYSIS
-- ============================================================

-- 4.1 Sales by Customer Segment
SELECT 
    Customer_Segment,
    COUNT(*) AS transaction_count,
    ROUND(SUM(Net_Sales), 2) AS total_revenue,
    ROUND(AVG(Net_Sales), 2) AS avg_spend
FROM retail_clean
GROUP BY Customer_Segment
ORDER BY total_revenue DESC;

-- 4.2 Most popular payment methods
SELECT 
    Payment_Method,
    COUNT(*) AS usage_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM retail_clean), 2) AS usage_pct,
    ROUND(SUM(Net_Sales), 2) AS total_revenue
FROM retail_clean
GROUP BY Payment_Method
ORDER BY usage_count DESC;

-- 4.3 Return rate analysis by category
SELECT 
    Category,
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN Return_Flag = 'Yes' THEN 1 ELSE 0 END) AS returns,
    ROUND(SUM(CASE WHEN Return_Flag = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS return_rate_pct
FROM retail_clean
GROUP BY Category
ORDER BY return_rate_pct DESC;

-- ============================================================
-- STEP 5: DISCOUNT IMPACT ANALYSIS
-- ============================================================

-- 5.1 Revenue impact of discounts
SELECT 
    Discount_Percent,
    COUNT(*) AS transactions,
    ROUND(SUM(Gross_Sales), 2) AS gross_revenue,
    ROUND(SUM(Discount_Amount), 2) AS total_discount_given,
    ROUND(SUM(Net_Sales), 2) AS net_revenue,
    ROUND(AVG(Quantity), 2) AS avg_units_per_order
FROM retail_clean
GROUP BY Discount_Percent
ORDER BY Discount_Percent;

-- 5.2 Which category benefits most from discounts?
SELECT 
    Category,
    ROUND(AVG(Discount_Percent), 2) AS avg_discount,
    ROUND(SUM(Discount_Amount), 2) AS total_discount_lost,
    ROUND(SUM(Net_Sales), 2) AS net_revenue
FROM retail_clean
GROUP BY Category
ORDER BY total_discount_lost DESC;

-- ============================================================
-- STEP 6: KPI SUMMARY (for Power BI Card visuals)
-- ============================================================

SELECT
    COUNT(*) AS total_transactions,
    ROUND(SUM(Net_Sales), 2) AS total_net_revenue,
    ROUND(SUM(Gross_Sales), 2) AS total_gross_revenue,
    ROUND(SUM(Discount_Amount), 2) AS total_discount_given,
    ROUND(AVG(Net_Sales), 2) AS avg_order_value,
    SUM(Quantity) AS total_units_sold,
    ROUND(SUM(CASE WHEN Return_Flag='Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*),2) AS overall_return_rate_pct
FROM retail_clean;
