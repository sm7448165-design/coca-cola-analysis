# Databricks notebook source
# TO BE COMPLETED: upload the original CSV to a permitted Databricks accessible volume/path.
# Set input_path to the actual location; no remote execution evidence exists yet.
input_path = "/Volumes/<catalog>/<schema>/<volume>/CocaCola_Inventory_Distribution_MySQL_Ready.csv"
from pyspark.sql import functions as F
raw = spark.read.option("header", True).option("inferSchema", True).csv(input_path)
assert raw.count() == 50000, "Import count does not match source; investigate"
assert len(raw.columns)==31
raw.printSchema()
raw.groupBy("Market").agg(F.sum("Sales_Revenue_USD").alias("revenue_usd"),F.sum("Demand_Units").alias("demand_units")).orderBy(F.desc("revenue_usd")).show(truncate=False)
raw.filter(F.col("Overstock_Flag")==1).groupBy("Market").count().show()
# Write Delta to a location you have permissions for (replace placeholders).
delta_path = "/Volumes/<catalog>/<schema>/<volume>/coca_cola_delta"
raw.write.format("delta").mode("overwrite").save(delta_path)
check=spark.read.format("delta").load(delta_path)
assert check.count()==raw.count()
display(check.limit(10))
# Capture dated screenshots of cell execution, table schema, count checks, and Delta table details.
