# Databricks notebook source
# DBTITLE 1,load data
csv_path = "/Volumes/adc_agent_copilot_dbx_rsc/intent_models/taxi_data/yellow_tripdata_example.csv"
df = spark.read.option("header", "true").csv(csv_path)
df.show(5)

# COMMAND ----------

# DBTITLE 1,create delta table
delta_path = "/Volumes/adc_agent_copilot_dbx_rsc/intent_models/taxi_data/delta_table"

df.write.format("delta").mode("overwrite").save(delta_path)


# COMMAND ----------

# DBTITLE 1,verify delta table
delta_path = "/Volumes/adc_agent_copilot_dbx_rsc/intent_models/taxi_data/delta_table"

# Read from the Delta folder
df = spark.read.format("delta").load(delta_path)
df.show(5)

# COMMAND ----------

# DBTITLE 1,update
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, delta_path)

# Set fare_amount to 0 where passenger_count is 0
delta_table.update(
    condition="passenger_count = '0'",
    set={"fare_amount": "'0.00'"}
)

# COMMAND ----------

# DBTITLE 1,delete
# Delete rows with trip_distance = 0
delta_table.delete("trip_distance = '0'")

# COMMAND ----------

# DBTITLE 1,merge
from pyspark.sql import Row

updates = spark.createDataFrame([
    Row(tpep_pickup_datetime="2019-01-01 00:21:00", passenger_count="1", fare_amount="99.99")
])

delta_table.alias("base").merge(
    updates.alias("updates"),
    "base.tpep_pickup_datetime = updates.tpep_pickup_datetime"
).whenMatchedUpdate(set={"fare_amount": "updates.fare_amount"}) \
 .whenNotMatchedInsert(values={
     "tpep_pickup_datetime": "updates.tpep_pickup_datetime",
     "passenger_count": "updates.passenger_count",
     "fare_amount": "updates.fare_amount"
}).execute()

# COMMAND ----------

# DBTITLE 1,time travel
# Read version 0 of the Delta table
df_v0 = spark.read.format("delta").option("versionAsOf", 0).load(delta_path)


# COMMAND ----------

# DBTITLE 1,verify time travel
# Read version 0 (before UPDATE and DELETE)
df_v0 = spark.read.format("delta").option("versionAsOf", 0).load(delta_path)
count_v0 = df_v0.count()

# Read current version (after UPDATE, DELETE, MERGE)
df_current = spark.read.format("delta").load(delta_path)
count_current = df_current.count()

# Show comparison
print(f"Row count before operations (version 0): {count_v0}")
print(f"Row count after operations (latest version): {count_current}")
