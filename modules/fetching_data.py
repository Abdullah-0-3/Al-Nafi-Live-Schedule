from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

class DataFetcher:
    def __init__(self, url):
        self.url = url

    def go_to_website(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Enable headless mode
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.url)
        return driver

    def extract_data(self):
        driver = self.go_to_website()
        time.sleep(5)  # Wait for the page to load, adjust as necessary
        element = driver.find_element(By.XPATH, '//*[@id="__nuxt"]/div/div[4]/div[2]/div')
        html_content = element.get_attribute('outerHTML')
        
        os.makedirs('modules/data', exist_ok=True)
        with open('modules/data/extracted_data.html', 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        driver.quit()

if __name__ == "__main__":
    url = 'http://alnafi.com/live-schedule'  # Replace with the actual URL
    fetcher = DataFetcher(url)
    fetcher.extract_data()
