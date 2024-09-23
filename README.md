# EPL_SCRAPER

This project scrapes Premier League match data from the `footballdatabase.eu` website and saves it as CSV files.

## Features

- Scrapes match data for multiple seasons of the Premier League.
- The number of seasons to scrape is determined by the value passed to the `extract_matches()` function.
- Saves match data in separate CSV files for each season.
- Uses Selenium to interact with the website dynamically.

## Requirements

To run this project, you need the following:
- Python 3.10+
- Selenium WebDriver
- Google Chrome and ChromeDriver

Alternatively, you can use Docker to avoid manual setup.

## Installation

### Option 1: Running with Docker

1. Make sure you have [Docker](https://www.docker.com/get-started) installed.
2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/epl-scraper.git
   ```
   
   ```bash
   cd epl-scraper
   ```
3. Build the Docker image:   
   ```bash
   docker build -t epl-scraper .
   ```
4. Run the scraper:
   ```bash
   docker run -v $(pwd)/outputs:/app/outputs epl-scraper
   ```
### Option 2: Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/epl-scraper.git
   cd epl-scraper
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Download ChromeDriver and add the path to the extract_matches function (replace the path in your code).
   
4.Run the script:
   ```bash
   python main.py
   ```


