import pytest
from unittest.mock import patch, MagicMock
import requests
from scraper import Scraper, CSVHandler, WebDriverManager

# Mock URLs and keywords for testing
sitemap_url = 'https://www.example.com/sitemap'
keywords = ['test', 'sample']

# Test Scraper functionality
class TestScraper:
    @patch('scraper.requests.Session.get')
    def test_extract_links(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
            <html><body>
                <a href="https://www.example.com/test1">Test1</a>
                <a href="https://www.example.com/test2">Test2</a>
            </body></html>
        '''
        mock_get.return_value = mock_response

        scraper = Scraper(sitemap_url, keywords)
        links = scraper.extract_links()
        assert len(links) == 2
        assert "test" in links[0]
        assert "test" in links[1]

    def test_invalid_sitemap_url(self):
        invalid_url = 'https://invalid-url'
        scraper = Scraper(invalid_url, keywords)
        links = scraper.extract_links()
        assert links == []

# Test CSVHandler functionality
class TestCSVHandler:
    def test_save_load_links(self, tmp_path):
        links = ['https://example.com/link1', 'https://example.com/link2']
        csv_file = tmp_path / "links.csv"

        # Test save to CSV
        CSVHandler.save_links_to_csv(links, csv_file)
        assert csv_file.exists()

        # Test load from CSV
        loaded_links = CSVHandler.load_links_from_csv(csv_file)
        assert len(loaded_links) == 2
        assert loaded_links[0] == 'https://example.com/link1'

# Test WebDriverManager functionality
class TestWebDriverManager:
    @patch('scraper.webdriver.Chrome')
    @patch('scraper.ChromeDriverManager.install')
    def test_get_driver(self, mock_install, mock_chrome):
        manager = WebDriverManager()
        driver = manager.get_driver()
        assert driver is not None
        assert mock_chrome.called
