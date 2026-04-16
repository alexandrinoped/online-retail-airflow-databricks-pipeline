from datetime import datetime

from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator

with DAG(
    dag_id="online_retail_pipeline",
    start_date=datetime(2026, 4, 14),
    schedule=None,
    catchup=False,
    tags=["airflow", "data-engineering", "databricks", "retail"],
) as dag:

    run_databricks_pipeline = DatabricksRunNowOperator(
        task_id="run_databricks_online_retail_job",
        databricks_conn_id="databricks_default",
        job_id=651552866452744,
    )