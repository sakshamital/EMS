import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Try to import Twilio, handle gracefully if not installed
try:
    from twilio.rest import Client
except ImportError:
    Client = None

load_dotenv()

class NotificationService:
    def __init__(self):
        # Load credentials from .env
        self.email_user = os.getenv("MAIL_USERNAME")
        self.email_pass = os.getenv("MAIL_PASSWORD")
        self.email_server = os.getenv("MAIL_SERVER", "smtp.gmail.com")
        self.email_port = int(os.getenv("MAIL_PORT", 587))
        
        self.twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")

    def send_email(self, to_email: str, subject: str, body: str):
        """Sends an email using SMTP. Prints to console if config is missing."""
        if not self.email_user or not self.email_pass:
            print(f"\n[MOCK EMAIL] To: {to_email}\nSubject: {subject}\nBody: {body}\n")
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.email_server, self.email_port)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            server.send_message(msg)
            server.quit()
            print(f"Email sent to {to_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def send_sms(self, to_phone: str, message: str):
        """Sends SMS using Twilio. Prints to console if config is missing."""
        if not self.twilio_sid or not self.twilio_token or not Client:
            print(f"\n[MOCK SMS] To: {to_phone}\nMessage: {message}\n")
            return

        try:
            client = Client(self.twilio_sid, self.twilio_token)
            client.messages.create(
                body=message,
                from_=self.twilio_phone,
                to=to_phone
            )
            print(f"SMS sent to {to_phone}")
        except Exception as e:
            print(f"Failed to send SMS: {e}")

# Create a single instance to be imported elsewhere
notifier = NotificationService()