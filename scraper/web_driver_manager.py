# scraper/web_driver_manager.py
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class WebDriverManager:
    def __init__(self):
        self.driver = None

    def get_driver(self):
        """Initializes and returns the Chrome WebDriver."""
        if self.driver is None:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')  # Run in headless mode (no GUI)
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            logging.info("WebDriver initialized")
        return self.driver

    def close_driver(self):
        """Closes the WebDriver if it's open."""
        if self.driver:
            self.driver.quit()
            logging.info("WebDriver closed")
