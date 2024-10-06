# scraper/csv_handler.py
import logging
import pandas as pd

class CSVHandler:
    @staticmethod
    def save_links_to_csv(links, filename):
        """Saves a list of unique links to a CSV file."""
        try:
            # Ensure links are unique by converting the list to a set
            unique_links = list(set(links))

            # Use pandas to write the links to a CSV
            df = pd.DataFrame(unique_links, columns=['Link'])

            # Save to CSV, without index column
            df.to_csv(filename, index=False, encoding='utf-8')

            logging.info(f"Successfully saved {len(unique_links)} links to {filename}")

        except Exception as e:
            logging.error(f"Error saving links to CSV: {e}")
    
    @staticmethod
    def load_links_from_csv(filename):
        """Loads links from a CSV file and returns a list of them."""
        try:
            df = pd.read_csv(filename)
            links = df['Link'].tolist()
            logging.info(f"Successfully loaded {len(links)} links from {filename}")
            return links
        except FileNotFoundError:
            logging.warning(f"File {filename} does not exist.")
            return []
        except Exception as e:
            logging.error(f"Error loading links from CSV: {e}")
            return []
