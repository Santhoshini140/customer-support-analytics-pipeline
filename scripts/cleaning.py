import pandas as pd


def trim_whitespace(df):
    """
    Removes leading and trailing spaces
    from all string columns.
    """

    string_columns = df.select_dtypes(include="object").columns

    for column in string_columns:
        df[column] = df[column].astype(str).str.strip()

    return df


def standardize_priority(df):
    """
    Standardizes priority values.
    """

    df["priority"] = (
        df["priority"]
        .str.title()
    )

    return df


def standardize_status(df):
    """
    Standardizes status values.
    """

    df["status"] = (
        df["status"]
        .str.title()
        .replace({
            "In progress": "In Progress"
        })
    )

    return df


def standardize_email(df):
    """
    Converts emails to lowercase.
    """

    df["customer_email"] = (
        df["customer_email"]
        .str.lower()
    )

    return df


def clean_customer_names(df):
    """
    Removes multiple spaces
    inside customer names.
    """

    df["customer_name"] = (
        df["customer_name"]
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
    )

    return df


def convert_dates(df):
    """
    Converts dates into datetime format.
    """

    df["created_date"] = pd.to_datetime(
        df["created_date"],
        errors="coerce"
    )

    df["resolved_date"] = pd.to_datetime(
        df["resolved_date"],
        errors="coerce"
    )

    return df


def convert_numeric_columns(df):
    """
    Converts numeric columns.
    """

    df["ticket_id"] = pd.to_numeric(
        df["ticket_id"],
        errors="coerce"
    )

    df["satisfaction_score"] = pd.to_numeric(
        df["satisfaction_score"],
        errors="coerce"
    )

    return df


def basic_cleaning(df):
    """
    Cleaning that should happen BEFORE validation.
    """

    df = trim_whitespace(df)
    df = standardize_priority(df)
    df = standardize_status(df)
    df = standardize_email(df)
    df = clean_customer_names(df)

    return df


def structural_cleaning(df):
    """
    Cleaning that should happen AFTER validation.
    """

    df = convert_dates(df)
    df = convert_numeric_columns(df)

    return df