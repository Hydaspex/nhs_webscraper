#nhs_webscraper

## Overview

This project is a web scraper designed to extract and compile data from the NHS My Planned Care website. The scraper utilizes Selenium for web automation and BeautifulSoup for parsing HTML. It extracts relevant waiting time information for various specialties, storing the data in a structured format for further analysis.

## Features

- **Web Automation**: Utilizes Selenium WebDriver to navigate and interact with web pages.
- **HTML Parsing**: Employs BeautifulSoup to extract and filter relevant links and data from the HTML content.
- **Data Extraction**: Extracts waiting time information for specific medical specialties, including providers and regions.
- **CSV Export**: Saves the extracted data to a CSV file, enabling easy data analysis and reporting.
- **Multi-threading**: Enhances performance by extracting data from multiple URLs simultaneously.

## Technologies Used

- **Python**: The primary programming language used for development.
- **Selenium**: A powerful tool for controlling web browsers through programs.
- **BeautifulSoup**: A Python library for parsing HTML and XML documents.
- **Pandas**: Used for data manipulation and exporting to CSV format.
- **Requests**: For making HTTP requests to fetch web pages.
- **GitHub Actions**: Continuous Integration (CI) setup for automated testing and deployment.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<username>/<repository-name>.git
   cd <repository-name>
