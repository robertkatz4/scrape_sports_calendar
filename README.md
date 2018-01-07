# Internet scrape/upload of sporting schedules into a single Google Calendar
The idea is to scrape league and team schedules, returning a list of dictionary objects, delete in a 'Sports' iCal existing matches in each schedule using the Google API, and then upload the scraped matches with appropriate notifications. As schedules change and teams advance, the project would refresh the Google Calendar with what I want to keep track of.


### Scrape of the schedules I care about
* #### NBA National Television Schedule
For the 2017-2018 NBA Season I abandoned the Scrapy project I used for 16-17 -
the new scraper hits the NBA's main schedule JSON API. Currently spitting out into csv for upload thru Google's UI, hitting the API would make this project far more useful.
* #### New York Knicks, God help me
Currently using some automatic download from the team's site
* #### Premier League's top six
Scrape of the Premier League's national television with only the teams I care
about - the top 6. Currently hitting the Guardian website and spitting out into csv for upload thru Google's UI, hitting the API would make this project far more useful.
* #### Manchester City, as of this writing at the top of the PL table
Premier League and Champions League, FA Cup, etc
This is perhaps the motivation for this project - I want this project to tee up the games for me in Google Calendar as they are early in the morning and I need the reminders.
* #### University of Oregon
* #### University of Michigan

---
Status 01.07.18: API calls work [delete/insert] with example event dictionaries from Google. The project needs to pass actual team schedules.

---

A few notes on the packages - I had to use the following as the most recent versions of each did not work. These have been added to the requirements.txt file.
xml==3.6.4
twisted=16.6.0
