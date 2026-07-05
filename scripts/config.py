# ==========================================================
# Google Cloud Configuration
# ==========================================================

PROJECT_ID = "abiding-robot-501314-d0"
DATASET_NAME = "customer_support"
TABLE_NAME = "customer_support_clean"
CREDENTIALS_PATH = "/opt/airflow/project/credentials/abiding-robot-501314-d0-1b28baf3241b.json"

# ==========================================================
# File Paths
# ==========================================================

RAW_DATA_PATH = "/opt/airflow/project/data/raw/customer_support_tickets.csv"

PROCESSED_FOLDER = "/opt/airflow/project/data/processed"
REJECTED_FOLDER = "/opt/airflow/project/data/rejected"
REPORT_FOLDER = "/opt/airflow/project/data/reports"