import pandas as pd
from sample_emailer import send_email
import os


def load_excel_data(file_path):
    return pd.ExcelFile(file_path)


def process_sheet(sheet_data, subject_template, sender_email):
    # Define the column patterns to search for
    column_patterns = {
        'sf_available': 'sf available',
        'agent_name': 'agent name',
        'subject_column': 'address',
        'email_column': 'email'
    }

    # Dictionary to store column names found
    columns_found = {}

    # Check for the existence of necessary columns in order to exectue program
    for key, pattern in column_patterns.items():
        matches = sheet_data.columns[sheet_data.columns.str.contains(
            pattern, case=False, na=False)]
        if matches.empty:
            raise ValueError(
                f"Column matching '{pattern}' does not exist in the sheet.")
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
        body = f"Hello {row[columns_found['agent_name']]}, {subject_template} {row[columns_found['sf_available']]}?"
        to_email = row[columns_found['email_column']]

        # Send the email
        send_email(subject, body, to_email)


def main():
    file_path = 'Proxy.xlsx'
    excel_data = load_excel_data(file_path)
    subject_template = os.getenv('SUBJECT')
    sender_email = os.getenv('SENDER_EMAIL')

    for sheet_name in excel_data.sheet_names:
        sheet_data = excel_data.parse(sheet_name)
        process_sheet(sheet_data, subject_template, sender_email)


if __name__ == "__main__":
    main()
