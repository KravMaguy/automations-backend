import pandas as pd

file_path = 'Proxy.xlsx'
excel_data = pd.ExcelFile(file_path)

for sheet_name in excel_data.sheet_names:
    sheet_data = excel_data.parse(sheet_name)
    print('sheeet data: ', sheet_data)
    email_column = sheet_data.columns[sheet_data.columns.str.contains(
        'email', case=False, na=False)]

    if not email_column.empty:
        print(f"Emails in sheet: {sheet_name}")
        for email in sheet_data[email_column[0]].dropna():
            print(email)
        print()
