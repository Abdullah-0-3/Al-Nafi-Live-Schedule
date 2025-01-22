import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
import os

class EmailSender:
    def __init__(self, from_email, from_password, smtp_server, smtp_port):
        self.from_email = from_email
        self.from_password = from_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, subject, body, to_email):
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.from_email, self.from_password)
        text = msg.as_string()
        server.sendmail(self.from_email, to_email, text)
        server.quit()

    def check_schedule_and_notify(self, json_file, to_email):
        today = datetime.today().strftime('%d-%m-%Y')
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for entry in data:
                dates = entry.get('Instructor')
                time = entry.get('Date')
                title = entry.get('No')
                if dates:
                    date_list = dates.split(', ')
                    if today in date_list:
                        subject = f"Reminder: Class Scheduled Today - {title}"
                        body = f"Dear Abdullah,\n\nThis is a reminder that you have a class scheduled today.\n\nTitle: {title}\nTime: {time}\n\nBest regards,\nYour School"
                        self.send_email(subject, body, to_email)

if __name__ == "__main__":
    load_dotenv()
    email_sender = EmailSender(
        from_email=os.getenv("EMAIL"),
        from_password=os.getenv("PASSWORD"),
        smtp_server=os.getenv("SMTP_SERVER"),
        smtp_port=int(os.getenv("SMTP_PORT"))
    )
    email_sender.check_schedule_and_notify('data/extracted_data.json', os.getenv("EMAIL"))
