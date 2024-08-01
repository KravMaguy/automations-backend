import unittest
from unittest.mock import patch
import pandas as pd
from pandas_agent import load_excel_data, process_sheet


class TestPandasAgent(unittest.TestCase):
    @patch('pandas_agent.send_email')  # Adjust this path as needed
    def test_process_sheet(self, mock_send_email):
        # Mock environment variables and set up test data
        subject_template = "What's the price per square foot for"
        sender_email = "default_sender@example.com"
        file_path = 'Proxy.xlsx'
        excel_data = load_excel_data(file_path)
        sheet_data = excel_data.parse(excel_data.sheet_names[0])

        # Run the processing function
        process_sheet(sheet_data, subject_template, sender_email)

        # Print debug info
        print("Captured calls:", mock_send_email.call_args_list)
        print("Call count:", mock_send_email.call_count)

        # Expected email recipients
        # needs to match email field values in the excel sheet
        expected_recipients = [
            'test1@gmail.com',
            'test2@gmail.com',
            'test3@companymail.com',
            'test4@costar.com'
        ]

        # Assertions
        self.assertEqual(mock_send_email.call_count, len(expected_recipients))
        actual_calls = [call[0][2] for call in mock_send_email.call_args_list]
        for email in expected_recipients:
            self.assertIn(email, actual_calls)


if __name__ == '__main__':
    unittest.main()
