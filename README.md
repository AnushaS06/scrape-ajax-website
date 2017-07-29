# Scraping AJAX Powered Website with Python

Script designed to use AJAX call to scrape AJAX power website without the use of Scrapy or Automated/Headless browser such as Selenium or Splash

It intercept AJAX calls and tries to reproduce and replay them using request library.

## Data Extracted

Visiting the following URL:
      www.wholefoodsmarket.com

The script extracts the following data and creates a JSON file as an output:

- Store name
- Full address
- Phone number
- Opening Hours
