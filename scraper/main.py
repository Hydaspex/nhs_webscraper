if __name__ == "__main__":
    sitemap_url = 'https://www.myplannedcare.nhs.uk/sitemap/'
    keywords = ['east', 'london', 'mids', 'ney', 'nwest', 'seast', 'swest']

    # Initialize the WebDriver using WebDriverManager
    driver_manager = WebDriverManager()
    driver = driver_manager.get_driver()

    start_time = time.time()

    try:
        scraper = Scraper(sitemap_url=sitemap_url, keywords=keywords)

        # Extract links from the sitemap
        links_to_scrape = scraper.extract_links(save_to_file='my_planned_care.csv')

        # Close the session once the requests are done
        scraper.close_session()

        # Initialize DataExtractor and start extracting data
        data_extractor = DataExtractor(driver)
        data_extractor.extract_data(links_to_scrape)

    except Exception as e:
        logging.error(f"Error in extracting data: {e}")

    finally:
        # Ensure the WebDriver is closed when scraping is complete
        driver_manager.close_driver()

    end_time = time.time()
    logging.info(f"Execution time: {end_time - start_time} seconds")
