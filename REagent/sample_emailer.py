import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def send_email(subject, body, to_email):
    # Gmail credentials from environment variables
    username = os.getenv('GMAIL_USER')
    password = os.getenv('GMAIL_PASSWORD')

    
    # Email content
    from_email = username

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to your Gmail account
        server.login(username, password)

        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())

        # Disconnect from the server
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")


# Example usage
# send_email('Test Subject', 'This is the body of the email',
#            'toEmail@email.com')
