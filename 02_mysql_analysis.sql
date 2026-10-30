-- MySQL 8+ | NOT EXECUTED ON MYSQL; expected outputs described separately.
USE coca_cola_supply_chain;

-- 01 Validate load
-- Expected: imported_rows, first_date, last_date
-- Interpretation: Compare imported count and range to original CSV.
SELECT COUNT(*) AS imported_rows, MIN(`Date`) AS first_date, MAX(`Date`) AS last_date FROM inventory_distribution;

-- 02 Demand, sales by market
-- Expected: Market, records, demand_units, units_sold, revenue_usd
-- Interpretation: Market priority by aggregated sales volume, not profit.
SELECT Market, COUNT(*) AS records, SUM(Demand_Units) AS demand_units, SUM(Units_Sold) AS units_sold, ROUND(SUM(Sales_Revenue_USD),2) AS revenue_usd FROM inventory_distribution GROUP BY Market ORDER BY revenue_usd DESC;

-- 03 Product revenue
-- Expected: Category, Product, units_sold, revenue_usd
-- Interpretation: Which products generate largest recorded revenue.
SELECT Category, Product, SUM(Units_Sold) AS units_sold, ROUND(SUM(Sales_Revenue_USD),2) AS revenue_usd FROM inventory_distribution GROUP BY Category,Product ORDER BY revenue_usd DESC;

-- 04 Forecast error
-- Expected: Market, mae_units, signed_error_units
-- Interpretation: MAE is row-level; do not assume forecast horizon.
SELECT Market, ROUND(AVG(ABS(Forecast_Demand_Units-Demand_Units)),2) AS mae_units, ROUND(SUM(Forecast_Demand_Units-Demand_Units),0) AS signed_error_units FROM inventory_distribution GROUP BY Market ORDER BY mae_units DESC;

-- 05 Overstock versus shortage flags
-- Expected: Market, rows_seen, overstock_flag_rows, stockout_flag_rows, overstock_flag_pct
-- Interpretation: Stock-outs are zero, not evidence that real-world stock-outs never occur.
SELECT Market, COUNT(*) AS rows_seen, SUM(Overstock_Flag) AS overstock_flag_rows, SUM(Stockout_Flag) AS stockout_flag_rows, ROUND(100*AVG(Overstock_Flag),2) AS overstock_flag_pct FROM inventory_distribution GROUP BY Market ORDER BY overstock_flag_pct DESC;

-- 06 Warehouse inventory
-- Expected: Warehouse_ID, rows_seen, mean_closing_units, holding_usd
-- Interpretation: Warehouse IDs may be shared across markets; verify meaning.
SELECT Warehouse_ID, COUNT(*) AS rows_seen, ROUND(AVG(Closing_Inventory_Units),2) AS mean_closing_units, SUM(Inventory_Holding_Cost_USD) AS holding_usd FROM inventory_distribution GROUP BY Warehouse_ID HAVING COUNT(*) > 0 ORDER BY holding_usd DESC;

-- 07 Transportation modes
-- Expected: Transport_Mode, journeys, mean_lead_days, total_transport_usd, avg_transport_usd, avg_distance_km
-- Interpretation: Costs are not directly comparable without distance and load adjustment.
SELECT Transport_Mode,COUNT(*) AS journeys,ROUND(AVG(Lead_Time_Days),2) AS mean_lead_days,ROUND(SUM(Transport_Cost_USD),2) AS total_transport_usd,ROUND(AVG(Transport_Cost_USD),2) AS avg_transport_usd,ROUND(AVG(Distance_KM),2) AS avg_distance_km FROM inventory_distribution GROUP BY Transport_Mode ORDER BY avg_transport_usd DESC;

-- 08 Country waste costs
-- Expected: Market, Country, waste_units, waste_usd
-- Interpretation: Identify waste-cost concentration.
SELECT Market,Country,SUM(Waste_Units) AS waste_units,ROUND(SUM(Waste_Cost_USD),2) AS waste_usd FROM inventory_distribution GROUP BY Market,Country ORDER BY waste_usd DESC LIMIT 20;

-- 09 Monthly demand
-- Expected: month, demand_units, revenue_usd
-- Interpretation: Date counts may differ; interpret aggregates as records observed.
SELECT DATE_FORMAT(`Date`,'%Y-%m') AS month, SUM(Demand_Units) AS demand_units,SUM(Sales_Revenue_USD) AS revenue_usd FROM inventory_distribution GROUP BY DATE_FORMAT(`Date`,'%Y-%m') ORDER BY month;

-- 10 Promotion and channel
-- Expected: Sales_Channel, Promotion, rows_seen, avg_row_revenue_usd
-- Interpretation: Association only; cannot establish promotions caused uplift.
SELECT Sales_Channel,Promotion, COUNT(*) AS rows_seen,ROUND(AVG(Sales_Revenue_USD),2) AS avg_row_revenue_usd FROM inventory_distribution GROUP BY Sales_Channel,Promotion ORDER BY avg_row_revenue_usd DESC;

-- 11 Inventory balance validation
-- Expected: mismatch_rows
-- Interpretation: Balance assumption may omit transfers/adjustments.
SELECT COUNT(*) AS mismatch_rows FROM inventory_distribution WHERE Opening_Inventory_Units+Production_Units-Units_Sold-Waste_Units <> Closing_Inventory_Units;

-- 12 Reorder candidates
-- Expected: Market, Product, Warehouse_ID, closing units, reorder point, reorder status
-- Interpretation: Row-level potential replenishment alerts, not approved purchase orders.
SELECT Market,Product,Warehouse_ID,Closing_Inventory_Units,Reorder_Point_Units, CASE WHEN Closing_Inventory_Units<=Reorder_Point_Units THEN 'At/below ROP' ELSE 'Above ROP' END AS reorder_status FROM inventory_distribution WHERE Closing_Inventory_Units<=Reorder_Point_Units ORDER BY Closing_Inventory_Units ASC LIMIT 100;

-- 13 Higher-than-average lead time
-- Expected: Market, mean_lead_days
-- Interpretation: CTE and scalar subquery; overall average is row-weighted.
WITH market_lead AS (SELECT Market,AVG(Lead_Time_Days) AS avg_lead FROM inventory_distribution GROUP BY Market) SELECT Market,ROUND(avg_lead,2) AS mean_lead_days FROM market_lead WHERE avg_lead>(SELECT AVG(Lead_Time_Days) FROM inventory_distribution) ORDER BY avg_lead DESC;

-- 14 Product ranking
-- Expected: Market, Product, revenue_usd, market_product_rank
-- Interpretation: Window ranking within each market.
SELECT Market,Product,SUM(Sales_Revenue_USD) AS revenue_usd,DENSE_RANK() OVER(PARTITION BY Market ORDER BY SUM(Sales_Revenue_USD) DESC) AS market_product_rank FROM inventory_distribution GROUP BY Market,Product;

-- 15 Conditional season summaries
-- Expected: Season, Holiday_Flag, rows_seen, no_promotion_rows, min_demand, max_demand, avg_demand
-- Interpretation: Descriptive seasonality, not causal holiday impact.
SELECT Season,Holiday_Flag,COUNT(*) AS rows_seen, SUM(CASE WHEN Promotion='No Promotion' THEN 1 ELSE 0 END) AS no_promotion_rows,MIN(Demand_Units) AS min_demand,MAX(Demand_Units) AS max_demand,AVG(Demand_Units) AS avg_demand FROM inventory_distribution GROUP BY Season,Holiday_Flag ORDER BY Season,Holiday_Flag;

-- 16 Example self-join of real grouping dimensions
-- Expected: Product, Category, Market, revenue_usd
-- Interpretation: JOIN demonstration using derived dimension sets; check uniqueness.
SELECT p.Product,p.Category,m.Market,SUM(f.Sales_Revenue_USD) AS revenue_usd FROM inventory_distribution f JOIN (SELECT DISTINCT Product,Category FROM inventory_distribution) p ON f.Product=p.Product AND f.Category=p.Category JOIN (SELECT DISTINCT Market FROM inventory_distribution) m ON f.Market=m.Market GROUP BY p.Product,p.Category,m.Market ORDER BY revenue_usd DESC LIMIT 20;

