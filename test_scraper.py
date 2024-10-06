import pytest
from unittest.mock import patch, Mock
from scraper import WebScraper
import requests

class TestWebScraper:
    @patch('scraper.requests.get')
    def test_fetch_page_success(self, mock_get):
        """
        Test the fetch_page method of the WebScraper class with a successful response.

        This test function mocks the requests.get method to return a mock response
        with a status code of 200 and a text containing a heading. It then creates
        an instance of the WebScraper class and calls the fetch_page method to fetch
        the mock response. Finally, it asserts that the fetched HTML is equal to the
        expected HTML.

        Parameters:
        - mock_get (MagicMock): A mock object of the requests.get method.

        Returns:
        None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><h1>Test Heading</h1></html>"
        mock_get.return_value = mock_response
        
        scraper = WebScraper("http://test.com")
        html = scraper.fetch_page()
        
        assert html == "<html><h1>Test Heading</h1></html>"
    
    @patch('scraper.requests.get')
    def test_fetch_page_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.HTTPError("404 Client Error")
        
        scraper = WebScraper("http://test.com")
        html = scraper.fetch_page()
        
        
        assert html is None
    
    @patch('scraper.requests.get')
    def test_parse_data(self, mock_get):
        """
        Test the parse_data method of the WebScraper class.

        This test function mocks the requests.get method to return a mock response
        with a status code of 200 and a text containing two headings. It then creates
        an instance of the WebScraper class and calls the scrape method to parse the
        mock response. Finally, it asserts that the parsed data is equal to a list
        containing the two headings.

        Parameters:
        - mock_get (MagicMock): A mock object of the requests.get method.

        Returns:
        None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><h1>Heading 1</h1><h1>Heading 2</h1></html>"
        mock_get.return_value = mock_response
        
        scraper = WebScraper("http://test.com")
        data = scraper.scrape()
        
        assert data == ["Heading 1", "Heading 2"]