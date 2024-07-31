import pandas as pd
from sample_emailer import send_email
import os


file_path = 'Proxy.xlsx'
excel_data = pd.ExcelFile(file_path)

for sheet_name in excel_data.sheet_names:
    sheet_data = excel_data.parse(sheet_name)
    # print(f"Processing {sheet_name}")

    # Define the column patterns to search for
    column_patterns = {
        'sf_available': 'sf available',
        'agent_name': 'agent name',
        'subject_column': 'address',
        'email_column': 'email'
    }

    # Dictionary to store column names found
    columns_found = {}
    email_subject = os.getenv('SUBJECT')

    # Check for the existence of necessary columns in order to exectue program
    for key, pattern in column_patterns.items():
        matches = sheet_data.columns[sheet_data.columns.str.contains(
            pattern, case=False, na=False)]
        if matches.empty:
            raise ValueError(
                f"Column matching '{pattern}' does not exist in the Excel sheet named '{sheet_name}'.")
        columns_found[key] = matches[0]
    for index, row in sheet_data.iterrows():
        missing_data = False
        for key in columns_found:
            if pd.isna(row[columns_found[key]]):
                missing_data = True
                break
        if missing_data:
            continue  # skip row with missing data

        subject = row[columns_found['subject_column']]
        body = f"Hello {row[columns_found['agent_name']]}, {email_subject} {row[columns_found['sf_available']]}?"
        to_email = row[columns_found['email_column']]
        print(f"Sending email to {to_email}")
        # send_email(subject, body, to_email)

    # print("-" * 40)
