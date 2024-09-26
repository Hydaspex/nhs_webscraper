import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, url):
        self.url = url

    def fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page: {e}")
            return None

    def parse_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        # Example: Extract all headings (h1)
        headings = [h1.text for h1 in soup.find_all('h1')]
        return headings

    def scrape(self):
        html = self.fetch_page()
        if html:
            return self.parse_data(html)
        return []