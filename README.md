# Intro
A scraper to scrape https://books.toscrape.com/

## Feature Set
- Built a Scrapy-based web scraper to collect book data from books.toscrape.com across all pages
- Extracted detailed fields such as title, price, rating, stock, availability, category, and description using XPath/CSS selectors.
- Implemented Pagination for complete data coverage.
- Used Scrapy pipelines to perform data cleaning and validation before storage.
- Integrated PostgreSQL as the backend database using psycopg2 for direct connection and storage.
- Developed custom middlewares with rotating proxies and randomized browser headers to avoid detection and ensure smooth crawling.
