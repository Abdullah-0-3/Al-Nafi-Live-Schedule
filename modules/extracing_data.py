from bs4 import BeautifulSoup
import csv
import json
import os

class DataExtractor:
    def __init__(self, html_file):
        self.html_file = html_file

    def extract_data(self):
        # Load the HTML content
        with open(self.html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extracting Headings
        headings = soup.find_all('thead')
        header = []
        for heading in headings:
            header = [cell.text.strip() for cell in heading.find_all('th')]

        # Extracting Data
        data = soup.find_all('tbody')
        rows_data = []
        for row in data:
            rows = row.find_all('tr')
            for tr in rows:
                cells = tr.find_all('td')
                row_data = [' '.join(cell.text.split()) for cell in cells]
                rows_data.append(row_data)

        # Ensure the data directory exists
        os.makedirs('modules/data', exist_ok=True)

        # Writing to CSV file
        with open('modules/data/extracted_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            if header:
                csvwriter.writerow(header)
            csvwriter.writerows(rows_data)

        # Writing to JSON file
        data_dict = [dict(zip(header, row)) for row in rows_data]
        with open('modules/data/extracted_data.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(data_dict, jsonfile, ensure_ascii=False, indent=4)