import os
from dotenv import load_dotenv
from modules.fetching_data import DataFetcher
from modules.extracing_data import DataExtractor
from modules.email_sender import EmailSender

def main():
    # Load environment variables
    load_dotenv()

    # Ensure the data directory exists
    os.makedirs('modules/data', exist_ok=True)

    # Fetch data
    fetcher = DataFetcher('http://alnafi.com/live-schedule')
    fetcher.extract_data()

    # Extract data
    extractor = DataExtractor('modules/data/extracted_data.html')
    extractor.extract_data()

    # Send email notifications
    email_sender = EmailSender(
        from_email=os.getenv("EMAIL"),
        from_password=os.getenv("PASSWORD"),
        smtp_server=os.getenv("SMTP_SERVER"),
        smtp_port=int(os.getenv("SMTP_PORT"))
    )
    email_sender.check_schedule_and_notify('modules/data/extracted_data.json', os.getenv("EMAIL"))

if __name__ == "__main__":
    main()
