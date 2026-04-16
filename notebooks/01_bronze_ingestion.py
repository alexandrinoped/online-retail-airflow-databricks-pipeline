from pyspark.sql.functions import current_timestamp, lit

RAW_FILE_PATH = "dbfs:/FileStore/online_retail/online_retail.csv"
BRONZE_PATH = "dbfs:/FileStore/online_retail/bronze/online_retail_raw"

df_raw = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(RAW_FILE_PATH)
)

if df_raw.count() == 0:
    raise ValueError("df_raw is empty")

df_bronze = (
    df_raw
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("source_file", lit("online_retail.csv"))
)

(
    df_bronze.write
    .mode("overwrite")
    .parquet(BRONZE_PATH)
)

print(f"Bronze layer created successfully at: {BRONZE_PATH}")
print(f"Row count: {df_bronze.count()}")