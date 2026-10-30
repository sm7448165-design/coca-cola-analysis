# Power BI dashboard specification — TO BE COMPLETED IN POWER BI
Import **the unchanged original CSV**; in Power Query set Date to Date, units to Whole Number and USD values to Decimal Number. Do not create a fact-table relationship without confirmed keys.

## KPI cards
- Revenue USD = SUM('inventory_distribution'[Sales_Revenue_USD])
- Demand units = SUM('inventory_distribution'[Demand_Units])
- Overstock flagged records = SUM('inventory_distribution'[Overstock_Flag])
- Stock-out count = SUM('inventory_distribution'[Stockout_Flag]) **(always zero; limitation)**
- Forecast MAE = AVERAGEX('inventory_distribution', ABS('inventory_distribution'[Forecast_Demand_Units]-'inventory_distribution'[Demand_Units]))

## Visuals (at least 4)
1. Horizontal bar: Revenue USD by Market
2. Column: Overstock flagged records (or share of rows) by Market
3. Line chart: Demand units and Forecast demand units by Date (month)
4. Clustered bars: Mean Lead_Time_Days by Transport_Mode; add Distance_KM as tooltip
5. Matrix: Product by Market, Revenue USD

Slicers: Market, Country, Product, Season, Promotion, Sales_Channel, Transport_Mode, Date.

## Required evidence
TO BE COMPLETED: upload actual .pbix or dashboard screenshots, confirm measures, filters, interaction and compare grand totals to the raw CSV. Nothing in this folder is evidence of a completed Power BI build.
