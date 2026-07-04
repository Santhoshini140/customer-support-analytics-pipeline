from scripts.processing import DataQualityEngine
from scripts.bigquery_loader import BigQueryLoader

engine = DataQualityEngine(
    "/opt/airflow/project/data/raw/customer_support_tickets.csv"
)

engine.process()

loader = BigQueryLoader(
    project_id="abiding-robot-501314-d0",
    dataset_name="customer_support",
    table_name="customer_support_clean",
    credentials_path="/opt/airflow/project/credentials/abiding-robot-501314-d0-1b28baf3241b.json"
)

loader.run(engine.clean_df)