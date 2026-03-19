# Reddit Data Scraper 🔍

A Python scraper that collects posts and user comments from Reddit using the public JSON API — no API key required.

## What it does
- Scrapes posts from multiple subreddits simultaneously
- Scrapes all comments from a specific Reddit user
- Filters comments by date range
- Generates incident IDs (IR-001, IR-002...) for each comment
- Identifies top-level comments vs replies
- Outputs to CSV

## Tech Stack
- Python 3.12
- Pandas
- Requests

## Project Structure
```
reddit-scraper/
├── scraper.py       # main scraper
└── requirements.txt
```

## How to run
```bash
git clone https://github.com/Delphineuzoeto/reddit-scraper.git
cd reddit-scraper
pip install -r requirements.txt
python scraper.py
```

## Usage
When prompted:
- Enter any Reddit username to scrape their comments
- Enter a start date (YYYY-MM-DD) to filter comments
- CSV saved as `{username}_comments.csv`
