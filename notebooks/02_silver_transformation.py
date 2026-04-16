from pyspark.sql.functions import col, to_timestamp, when, lit

BRONZE_PATH = "dbfs:/FileStore/online_retail/bronze/online_retail_raw"
SILVER_PATH = "dbfs:/FileStore/online_retail/silver/online_retail_clean"

df_bronze = spark.read.parquet(BRONZE_PATH)

if df_bronze.count() == 0:
    raise ValueError("df_bronze is empty")

df_silver = (
    df_bronze
    .withColumn("InvoiceDate", to_timestamp(col("InvoiceDate"), "M/d/yyyy H:mm"))
    .withColumn("CustomerID", col("CustomerID").cast("string"))
    .withColumn("Quantity", col("Quantity").cast("int"))
    .withColumn("UnitPrice", col("UnitPrice").cast("double"))
    .withColumn("total_amount", col("Quantity") * col("UnitPrice"))
    .withColumn(
        "invoice_status",
        when(col("InvoiceNo").startswith("C"), lit("Cancelled"))
        .when(col("Quantity") < 0, lit("Return"))
        .when(
            (col("Quantity") > 0) &
            (col("UnitPrice") > 0) &
            (~col("InvoiceNo").startswith("C")),
            lit("Sale")
        )
        .otherwise(lit("Invalid"))
    )
    .withColumn(
        "customer_status",
        when(col("CustomerID").isNull(), lit("Unidentified"))
        .otherwise(lit("Identified"))
    )
    .withColumn(
        "item_status",
        when(col("Description").isNull(), lit("Inconsistent"))
        .otherwise(lit("Valid"))
    )
)

(
    df_silver.write
    .mode("overwrite")
    .parquet(SILVER_PATH)
)

print(f"Silver layer created successfully at: {SILVER_PATH}")
print(f"Row count: {df_silver.count()}")