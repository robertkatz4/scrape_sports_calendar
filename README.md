Scrape of the NBA's national television with only the channels I care about
  as of March 1 the site changed and the scraper no longer works ¯\_(ツ)_/¯

Scrape of the Premier League's national television with only the teams I care about - the top 6. The idea is to return a JSON file from the Scrapy scraper
can be run with
python scrape_sports_api/spiders/spider_premier_league.py

and then upload the JSON file into the GCAL API, with a loop.

A few notes on the packages - I had to use the following as the most recent versions of each did not work. These have been added to the requirements.txt file.
xml==3.6.4
twisted=16.6.0
