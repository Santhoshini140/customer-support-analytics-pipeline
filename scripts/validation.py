import re
import pandas as pd

# ==========================================================
# Configuration
# ==========================================================

REQUIRED_COLUMNS = [
    "ticket_id",
    "customer_name",
    "customer_email",
    "issue_type",
    "priority",
    "status",
    "agent_name",
    "created_date",
    "resolved_date",
    "satisfaction_score"
]

MANDATORY_COLUMNS = [
    "ticket_id",
    "customer_name",
    "customer_email",
    "issue_type",
    "priority",
    "status"
]

VALID_PRIORITIES = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

VALID_STATUS = [
    "Open",
    "In Progress",
    "Resolved",
    "Closed"
]

EMAIL_PATTERN = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'


# ==========================================================
# Helper Function
# ==========================================================

# ==========================================================
# Helper Function
# ==========================================================

def validation_result(
    name,
    df,
    failed_indices,
    reason,
    severity="FAIL"
):
    """
    Creates a standard validation result dictionary.
    """

    ticket_ids = (
        df.loc[failed_indices, "ticket_id"]
        .astype(str)
        .tolist()
    )

    failed_count = len(failed_indices)

    if failed_count == 0:
        status = "PASS"
    else:
        status = severity

    return {
        "validation": name,
        "status": status,
        "failed_rows": failed_count,
        "invalid_ticket_ids": ticket_ids,
        "reason": "" if failed_count == 0 else reason
    }



# ==========================================================
# 1. Schema Validation
# ==========================================================

def check_required_columns(df):

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    return {
        "validation": "Required Columns",
        "status": "PASS" if len(missing_columns) == 0 else "FAIL",
        "failed_rows": len(missing_columns),
        "missing_columns": missing_columns
    }


# ==========================================================
# 2. Missing Values
# ==========================================================

def check_missing_values(df):

    results = []

    for column in MANDATORY_COLUMNS:

        failed = df[df[column].isnull()].index.tolist()

        results.append(
            validation_result(
                f"Missing Values - {column}",
                df,
                failed,
                f"Missing Values - {column}"
            )
        )

    return results


# ==========================================================
# 3. Duplicate Ticket IDs
# ==========================================================

def check_duplicate_ticket_ids(df):

    failed = df[df.duplicated(subset=["ticket_id"], keep=False)].index.tolist()

    return validation_result(
        "Duplicate Ticket IDs",
        df,
        failed,
        "Duplicate Ticket id"
    )


# ==========================================================
# 4. Allowed Priorities
# ==========================================================

def check_priority_values(df):

    failed = df[
        ~df["priority"].isin(VALID_PRIORITIES)
    ].index.tolist()

    return validation_result(
        "Priority Validation",
        df,
        failed,
        "Invalid Priority"
    )


# ==========================================================
# 5. Allowed Status
# ==========================================================

def check_status_values(df):

    failed = df[
        ~df["status"].isin(VALID_STATUS)
    ].index.tolist()

    return validation_result(
        "Status Validation",
        df,
        failed,
        "Invalid Status"
    )


# ==========================================================
# 6. Email Validation
# ==========================================================

def check_email_format(df):

    failed = []

    for idx, email in df["customer_email"].items():

        if pd.isna(email):
            continue

        if re.match(EMAIL_PATTERN, str(email)) is None:
            failed.append(idx)

    return validation_result(
        "Email Validation",
        df,
        failed,
        "Invalid Email"
    )


# ==========================================================
# 7. Date Validation
# ==========================================================

def check_date_validation(df):

    failed = []

    today = pd.Timestamp.today()

    created = pd.to_datetime(
        df["created_date"],
        errors="coerce"
    )

    resolved = pd.to_datetime(
        df["resolved_date"],
        errors="coerce"
    )

    for idx in df.index:

        if pd.notna(created[idx]):

            if created[idx] > today:
                failed.append(idx)
                continue

        if pd.notna(created[idx]) and pd.notna(resolved[idx]):

            if resolved[idx] < created[idx]:
                failed.append(idx)

    return validation_result(
        "Date Validation",
        df,
        failed,
        "Invalid Date"
    )


# ==========================================================
# 8. Business Rules
# ==========================================================

def check_business_rules(df):

    failed = []

    for idx, row in df.iterrows():

        status = row["status"]

        resolved = row["resolved_date"]

        score = row["satisfaction_score"]

        if status == "Open":

            if pd.notna(resolved):
                failed.append(idx)
                continue

        if status in ["Resolved", "Closed"]:

            if pd.isna(resolved):
                failed.append(idx)
                continue

        if pd.notna(score):

            if status not in ["Resolved", "Closed"]:
                failed.append(idx)

    return validation_result(
    "Business Rules",
    df,
    failed,
    "Business Rule Warning",
    severity="WARNING"
)