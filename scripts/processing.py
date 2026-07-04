import os
from datetime import datetime

import pandas as pd

from scripts.validation import (
    check_required_columns,
    check_missing_values,
    check_duplicate_ticket_ids,
    check_priority_values,
    check_status_values,
    check_email_format,
    check_date_validation,
    check_business_rules,
)

from scripts.cleaning import (
    basic_cleaning,
    structural_cleaning,
)


class DataQualityEngine:

    def __init__(self, input_file):

        self.input_file = input_file

        self.df = None

        self.validation_results = []

        self.rejection_map = {}

        self.warning_map = {}

        self.clean_df = None

        self.rejected_df = None

        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.output_dirs = {
            "processed": "data/processed",
            "rejected": "data/rejected",
            "reports": "data/reports"
        }

        self.create_output_directories()
    def create_output_directories(self):

        """
        Creates output folders if they don't already exist.
        """

        for folder in self.output_dirs.values():
            os.makedirs(folder, exist_ok=True)

    def load_data(self):

        """
        Reads the raw CSV.
        """

        print("\nLoading dataset...")

        self.df = pd.read_csv(self.input_file)

        print(f"Rows Loaded : {len(self.df)}")

    def validate(self):

        """
        Runs every validation.
        """

        print("\nRunning validations...")

        results = []

        schema_result = check_required_columns(self.df)

        results.append(schema_result)

        if schema_result["status"] == "FAIL":

            self.validation_results = results

            return

        results.extend(
            check_missing_values(self.df)
        )

        results.append(
            check_duplicate_ticket_ids(self.df)
        )

        results.append(
            check_priority_values(self.df)
        )

        results.append(
            check_status_values(self.df)
        )

        results.append(
            check_email_format(self.df)
        )

        results.append(
            check_date_validation(self.df)
        )

        results.append(
            check_business_rules(self.df)
        )

        self.validation_results = results  

    def build_rejection_map(self):
        """
        Builds a dictionary of rejected ticket IDs
        and all reasons they failed validation.
        """

        print("\nBuilding rejection map...")

        self.rejection_map = {}

        for result in self.validation_results:

            if result["status"] != "FAIL":
                continue

            if "invalid_ticket_ids" not in result:
                continue

            for ticket_id in result["invalid_ticket_ids"]:

                if ticket_id not in self.rejection_map:
                    self.rejection_map[ticket_id] = []

                self.rejection_map[ticket_id].append(result["reason"])

    def build_warning_map(self):

        print("\nBuilding warning map...")

        self.warning_map = {}

        for result in self.validation_results:

            if result["status"] != "WARNING":
                continue

            for ticket_id in result["invalid_ticket_ids"]:

                self.warning_map.setdefault(ticket_id, [])

                self.warning_map[ticket_id].append(result["reason"])


    def split_valid_invalid(self):
        """
        Separates clean and rejected records.
        """

        print("\nSeparating valid and rejected records...")

        rejected_ticket_ids = set(self.rejection_map.keys())

        self.rejected_df = self.df[
            self.df["ticket_id"].astype(str).isin(rejected_ticket_ids)
        ].copy()

        self.clean_df = self.df[
            ~self.df["ticket_id"].astype(str).isin(rejected_ticket_ids)
        ].copy()

        if not self.rejected_df.empty:

            self.rejected_df["rejection_reason"] = (
                self.rejected_df["ticket_id"]
                .astype(str)
                .map(
                    lambda x: ", ".join(self.rejection_map[x])
                )
            )

    def clean(self):
        """
        Cleans only valid records.
        """

        print("\nRunning structural cleaning...")

        self.clean_df = structural_cleaning(self.clean_df)

    def add_warning_column(self):
        """
        Adds warning information to the clean dataset.
        """

        print("\nAdding data quality warning column...")

        self.clean_df["data_quality_warning"] = (
            self.clean_df["ticket_id"]
            .astype(str)
            .map(
                lambda x: ", ".join(self.warning_map[x])
                if x in self.warning_map
                else ""
            )
        )


    def generate_validation_report(self):
        """
        Creates validation summary report.
        """

        print("\nGenerating validation report...")

        report = pd.DataFrame(self.validation_results)

        report["total_rows"] = len(self.df)

        report["pass_percentage"] = (
            (
                len(self.df) - report["failed_rows"]
            )
            / len(self.df)
            * 100
        ).round(2)

        report.to_csv(
            f"data/reports/validation_report_{self.timestamp}.csv",
            index=False
        )

    def save_outputs(self):
        """
        Saves clean and rejected datasets.
        """

        print("\nSaving outputs...")

        self.clean_df.to_csv(
            f"data/processed/customer_support_clean_{self.timestamp}.csv",
            index=False
        )

        self.rejected_df.to_csv(
            f"data/rejected/rejected_records_{self.timestamp}.csv",
            index=False
        )

    
    def process(self):
        """
        Executes the complete data quality pipeline.
        """

        self.load_data()

        # Normalize before validation
        self.df = basic_cleaning(self.df)

        self.validate()

        self.build_rejection_map()

        self.build_warning_map()

        self.split_valid_invalid()

        self.clean()

        self.add_warning_column()

        self.generate_validation_report()

        self.save_outputs()

        print("\n===================================")
        print("Data Quality Engine Completed")
        print("===================================")
        print(f"Total Records     : {len(self.df)}")
        print(f"Valid Records     : {len(self.clean_df)}")
        print(f"Rejected Records  : {len(self.rejected_df)}")