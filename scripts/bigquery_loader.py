from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from scripts.config import (
    PROJECT_ID,
    DATASET_NAME,
    TABLE_NAME,
    CREDENTIALS_PATH
)

class BigQueryLoader:

    def __init__(self):

        self.project_id = PROJECT_ID
        self.dataset_name = DATASET_NAME
        self.table_name = TABLE_NAME
        self.credentials_path = CREDENTIALS_PATH

        self.client = None

    def authenticate(self):
        """
        Authenticates using the service account.
        """

        print("\nAuthenticating with Google Cloud...")

        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path
        )

        self.client = bigquery.Client(
            project=self.project_id,
            credentials=credentials
        )

        print("Authentication Successful.")

    def upload_dataframe(self, df):
        """
        Uploads a Pandas DataFrame to BigQuery.
        """

        print("\nUploading DataFrame to BigQuery...")

        table_id = (
            f"{self.project_id}."
            f"{self.dataset_name}."
            f"{self.table_name}"
        )

        job = self.client.load_table_from_dataframe(
            df,
            table_id
        )

        job.result()

        print(f"Upload completed successfully.")

        table = self.client.get_table(table_id)

        print(f"Rows in BigQuery : {table.num_rows}")

    def run(self, df):

        self.authenticate()

        self.upload_dataframe(df)