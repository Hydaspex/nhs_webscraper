# scraper/data_extractor.py
import logging
from threading import Lock
import pandas as pd
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class DataExtractor:
    def __init__(self, driver):
        self.driver = driver
        self.lock = Lock()  # Ensures thread-safe access to shared data
        self.success_count = 0
        self.failure_count = 0
        self.provider_set = set()  # To keep track of unique providers
        logging.info(f"DataExtractor initialized with driver: {driver}")

    def process_url(self, link):
        """Extracts data from a given URL."""
        specs, specs_txt, providers, regions, weeks, metrics = [], [], [], [], [], []
        wait = WebDriverWait(self.driver, 4)

        try:
            if isinstance(link, str) and link.strip():
                logging.info(f"Processing URL: {link}")
                self.driver.get(link)

                try:
                    # Wait for provider and region elements to appear
                    provider_elem = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/nav/div/ol/li[3]")))
                    region_elem = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/nav/div/ol/li[2]/a")))

                    provider = provider_elem.get_attribute('innerText')
                    region = region_elem.get_attribute('innerText')

                    logging.info(f"Provider: {provider}, Region: {region}")

                    # Add the provider to the set for uniqueness
                    self.provider_set.add(provider)

                except Exception as e:
                    logging.error(f"Error finding provider or region in {link}: {e}")
                    with self.lock:
                        self.failure_count += 1
                    return [], [], [], [], []

                elements = self.driver.find_elements(By.CLASS_NAME, "nav-item-from-list")

                if elements:
                    for element in elements:
                        spec_link = element.get_attribute('href')
                        spec_text = element.get_attribute('innerText')

                        if spec_link and spec_link.startswith("http"):
                            specs.append(spec_link)
                            specs_txt.append(spec_text)

                            with self.lock:
                                providers.append(provider)  
                                regions.append(region)

                            logging.info(f"Specialty: {spec_text}, URL: {spec_link}")
                        else:
                            logging.error(f"Invalid specialty URL: {spec_link}")

                    for spec in specs:
                        try:
                            self.driver.get(spec)
                            logging.info(f"Navigating to specialty page: {spec}")

                            values = self.driver.find_elements(By.XPATH, "//table[@class='waiting-times-data']/tr/td")

                            if len(values) > 1:
                                week = values[1].get_attribute('innerText')
                                weeks.append(week)
                                metrics.append("Average waiting time for treatment at this hospital for this specialty")
                                logging.info(f"Extracted week: {week}")
                            else:
                                weeks.append("n/a")
                                metrics.append("n/a")
                        except Exception as e:
                            logging.error(f"Error extracting specialty data from {spec}: {e}")
                            weeks.append("n/a")
                            metrics.append("n/a")

                with self.lock:
                    self.success_count += 1
                return regions, providers, specs_txt, weeks, metrics

        except Exception as e:
            logging.error(f"Error processing {link}: {e}")
            with self.lock:
                self.failure_count += 1

        return [], [], [], [], []
