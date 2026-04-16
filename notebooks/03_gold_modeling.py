from pyspark.sql.functions import col, min, max, countDistinct, sum, datediff, current_date

SILVER_PATH = "dbfs:/FileStore/online_retail/silver/online_retail_clean"

GOLD_FACT_SALES_PATH = "dbfs:/FileStore/online_retail/gold/fact_sales"
GOLD_DIM_CUSTOMER_PATH = "dbfs:/FileStore/online_retail/gold/dim_customer"
GOLD_AGG_RFM_CUSTOMER_PATH = "dbfs:/FileStore/online_retail/gold/agg_rfm_customer"

df_silver = spark.read.parquet(SILVER_PATH)

if df_silver.count() == 0:
    raise ValueError("df_silver is empty")

df_sales = df_silver.filter(col("invoice_status") == "Sale")

df_fact_sales = df_sales.select(
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
    "total_amount",
    "invoice_status"
)

df_dim_customer = (
    df_sales
    .filter(col("CustomerID").isNotNull())
    .groupBy("CustomerID")
    .agg(
        min("InvoiceDate").alias("first_purchase_date"),
        max("InvoiceDate").alias("last_purchase_date"),
        countDistinct("InvoiceNo").alias("total_orders"),
        sum("total_amount").alias("total_revenue")
    )
)

df_rfm_customer = (
    df_sales
    .filter(col("CustomerID").isNotNull())
    .groupBy("CustomerID")
    .agg(
        datediff(current_date(), max("InvoiceDate")).alias("recency_days"),
        countDistinct("InvoiceNo").alias("frequency"),
        sum("total_amount").alias("monetary")
    )
)

(
    df_fact_sales.write
    .mode("overwrite")
    .parquet(GOLD_FACT_SALES_PATH)
)

(
    df_dim_customer.write
    .mode("overwrite")
    .parquet(GOLD_DIM_CUSTOMER_PATH)
)

(
    df_rfm_customer.write
    .mode("overwrite")
    .parquet(GOLD_AGG_RFM_CUSTOMER_PATH)
)

print(f"Gold fact_sales created at: {GOLD_FACT_SALES_PATH}")
print(f"Gold dim_customer created at: {GOLD_DIM_CUSTOMER_PATH}")
print(f"Gold agg_rfm_customer created at: {GOLD_AGG_RFM_CUSTOMER_PATH}")