# scraper/scraper.py
import logging
import random
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from scraper.csv_handler import CSVHandler

class Scraper:
    def __init__(self, sitemap_url, keywords):
        self.sitemap_url = sitemap_url
        self.keywords = keywords

        # Create a session with increased pool size
        self.session = requests.Session()
        adapter = HTTPAdapter(pool_connections=2, pool_maxsize=10, max_retries=Retry(total=3))  # Increased pool size
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def extract_links(self, save_to_file=None):
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/85.0'
            ])
        }

        try:
            # Use the session to send a GET request
            response = self.session.get(self.sitemap_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [str(link.get('href')) for link in soup.find_all('a') if link.get('href')]

            # Filter links based on keywords and exactly three slashes
            filtered_links = [
                link for link in links
                if any(keyword in link for keyword in self.keywords) and link.count('/') > 4
            ]

            if all(isinstance(link, str) for link in filtered_links):
                logging.info("All extracted links are in string format.")
            else:
                logging.warning("Some extracted links are not in string format.")

            # Save to CSV if filename is provided
            if save_to_file:
                CSVHandler.save_links_to_csv(filtered_links, save_to_file)

            return filtered_links

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching the sitemap: {e}")
            return []

    def close_session(self):
        """Close the session after all requests are completed."""
        self.session.close()
