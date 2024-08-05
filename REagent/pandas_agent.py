import pandas as pd
from sample_emailer import send_email
import os

def load_excel_data(file_path):
    return pd.ExcelFile(file_path)

def process_sheet(sheet_data, subject_template, sender_email):
    column_patterns = {
        'sf_available': 'sf available',
        'agent_name': 'agent name',
        'subject_column': 'address',
        'email_column': 'email'
    }

    columns_found = {}

    for key, pattern in column_patterns.items():
        matches = sheet_data.columns[sheet_data.columns.str.contains(pattern, case=False, na=False)]
        if matches.empty:
            raise ValueError(f"Column matching '{pattern}' does not exist in the sheet.")
        columns_found[key] = matches[0]

    last_address = None

    for index, row in sheet_data.iterrows():
        missing_data = False
        for key in columns_found:
            if pd.isna(row[columns_found[key]]) and key != 'subject_column':
                missing_data = True
                break

        if missing_data:
            continue  # skip row with missing data

        if not pd.isna(row[columns_found['subject_column']]):
            last_address = row[columns_found['subject_column']]

        if last_address is None:
            continue  # skip if there's no initial address

        subject = last_address
        sqFtInt = int(row[columns_found['sf_available']])
        body = f"Hello {row[columns_found['agent_name']]}, {subject_template} {sqFtInt}?"
        to_email = row[columns_found['email_column']]

        send_email(subject, body, to_email)

def main(file_path):
    excel_data = load_excel_data(file_path)
    subject_template = os.getenv('SUBJECT')
    sender_email = os.getenv('SENDER_EMAIL')

    for sheet_name in excel_data.sheet_names:
        try:
            sheet_data = excel_data.parse(sheet_name)
            print(f"Processing sheet '{sheet_name}'\n")
            process_sheet(sheet_data, subject_template, sender_email)
        except ValueError as e:
            print(f"Error processing sheet '{sheet_name}': {e}")

if __name__ == "__main__":
    main('Proxy.xlsx')  # Default value for testing
