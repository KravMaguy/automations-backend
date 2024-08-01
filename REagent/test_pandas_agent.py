import unittest
from unittest.mock import patch
import pandas as pd
import os
import json
from dotenv import load_dotenv
from pandas_agent import load_excel_data, process_sheet

load_dotenv(dotenv_path='.env.test')  # Load the test-specific .env file


class TestPandasAgent(unittest.TestCase):
    @patch('pandas_agent.send_email')  # Adjust this path as needed
    def test_process_sheet(self, mock_send_email):
        recipients_json = os.getenv('EXPECTED_RECIPIENTS')
        # Expected email recipients
        # needs to match VALID email field values in the excel sheet
        # pandas_agent defines what is valid as values that 
        expected_recipients = json.loads(recipients_json)

        # Mock environment variables and set up test data
        subject_template = "What's the price per square foot for"
        sender_email = "default_sender@example.com"
        file_path = 'Proxy.xlsx'
        excel_data = load_excel_data(file_path)
        sheet_data = excel_data.parse(excel_data.sheet_names[0])

        for sheet_name in excel_data.sheet_names:
            sheet_data = excel_data.parse(sheet_name)
            process_sheet(sheet_data, subject_template, sender_email)

        # Print debug info
        print("Captured calls:", mock_send_email.call_args_list)
        print("Call count:", mock_send_email.call_count)

        # Check if send_email was called the correct number of times
        self.assertEqual(mock_send_email.call_count, len(expected_recipients))
        actual_calls = [call[0][2] for call in mock_send_email.call_args_list]
        for email in expected_recipients:
            self.assertIn(email, actual_calls)


if __name__ == '__main__':
    unittest.main()
