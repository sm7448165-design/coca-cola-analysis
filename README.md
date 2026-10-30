# Coca-Cola Inventory & Distribution — PGDM Big Data Analytics / DBMS

## Status and honesty
- CSV source: user-supplied academic project file; external provenance **TO BE COMPLETED**.
- Original CSV retained unchanged (SHA-256 `eb4c0a011af2ab56b8fe9e82d08400cea6893a699703bffd62698db6e6d1d7dc`).
- Python/pandas source audit and charts **COMPLETED locally**. SQL script **NOT executed on MySQL**; Databricks/Delta Lake **NOT executed**; Power BI **NOT built**.
- Faculty guideline PDF asks for PostgreSQL; this version intentionally uses **MySQL**. Obtain faculty approval.
- There are 50,000 records, 31 source fields, and no exact duplicates/nulls.
- All `Stockout_Flag=0`, `Fill_Rate_Percent=100`, and `Demand_Units=Units_Sold`. Avoid unwarranted service claims.
- 3,841 records fail the assumed basic inventory reconciliation; no repair performed.

## Files and reproducibility
- `data/` original raw CSV, `data_dictionary.csv`, `data_audit_and_dictionary.xlsx`, verified aggregated summary CSVs, and audit metadata
- `sql/01_mysql_schema.sql`: MySQL 8+ DDL; run in DBeaver after creating a connection.
- `sql/02_mysql_analysis.sql`: 16 MySQL queries; `query_catalogue.csv` interpretation catalogue.
- `python/coca_cola_analysis.ipynb`: open Jupyter from `python/`, run all cells. Requires pandas, numpy, matplotlib, notebook.
- `python/chart_*.png`: 4 charts actually produced from source CSV.
- `databricks/databricks_delta_workflow.py`: code template to execute after supplying cloud file paths.
- `powerbi/dashboard_spec.md`: DAX measures and dashboard design; build + capture evidence.
- `report/Coca_Cola_Evidence_Based_Project_Report.pdf`: working analytical report; not a fabricated final deployment report.
- `presentation/`: evidence-grounded initial slide deck.

## MySQL CSV import
1. In DBeaver connect to MySQL 8+. Run `sql/01_mysql_schema.sql`.
2. Import the CSV using DBeaver's CSV wizard, mapping the 31 source columns in order, excluding generated `row_id`.
3. Confirm Date parsed as DATE in `YYYY-MM-DD` format and numeric decimal precision; confirm 50,000 imported records.
4. Execute the validation and analysis queries and save outputs/screenshots.
5. The default schema has no forced FK relationships because table grain and dimension IDs are not documented.

## What is still required for final submission
True provenance and source rights; faculty acceptance of MySQL; MySQL/DBeaver execution proof; Databricks/Delta run evidence; PBIX screenshots and validation; GitHub repository URL; named team contributions; faculty-specific approximately 30-page report expansion and recorded/live demo.

## Verified totals
Revenue USD 9,991,731.05, demand units 11,472,087, overstock flags 42,598, transport USD 478,330.34, waste USD 33,120.34.
