# Author: Robert Katz
# Version: 0.1, python 2.7.12
# Program description: Scrapy. This scrapes the NBA national TV schedule from the NBA website using Scrapy, a Python-based
###### web scraper, and outputs a CSV for direct upload into a Google Calendar.
###### It's valuable to me because the scraper can update the schedule with a few clicks, so the TV schedule
###### reflects the league's changes. As a KNicks fan whose twam is constantly moved off the schedule, this is useful.
###### Also, the scraper takes out all the Canadian national tv games, as well as all the League Pass games,
###### both of which are listed on the website. NBA TV games are included - I have that. :)
# output: csv
# Revision history:
# next step: maybe remove NBATV games or allow user to specify channels on the command line
# change for github
#another change

import scrapy
from datetime import *

class ScheduleSpider(scrapy.Spider):
    name = "nba"
    start_urls = [
        'http://www.nba.com/schedules/national_tv_schedule/',
    ]

    def parse(self, response):
        foo = response.css('#scheduleMain > table tr:nth-child(n+3)')
        for game in foo:
            # subject
            host = game.css('a:nth-child(2)::text').extract()[0]
            visitor = game.css('a:nth-child(1)::text').extract()[0]
            g=" "
            seq = (visitor,"@",host)
            heading = g.join(seq)
            # add date to blank date fields
            # one line could be removed
            dt_var = game.css('td.dt::text').extract()[0]
            # blank dates removed
            if dt_var[0] != " ":
                previous_date = dt_var
            else:
                dt_var = previous_date
            # date converted to dd/mm/yyyy
            months = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)
            month_int = months[dt_var[dt_var.find(", ")+2:dt_var.find(" ",dt_var.find(", ")+4)]]
            day_int = int(dt_var[dt_var.find(" ",7)+1:len(dt_var)])
            if month_int < 8:
                dt_var = date(2017,month_int, day_int)
            else:
                dt_var = date(2016,month_int, day_int)
            dt_var = dt_var.strftime('%m/%d/%Y')

            # channel
            ntv_var = game.css('img::attr(src)').extract()
            if ntv_var == []:
                s = ",."
            else:
                s = ntv_var[0]
            channel=s[s.find("_")+1:s.find(".",s.find("_"))]
            #time
            time_str = game.css('td.tm::text').extract()[0]
            time_var = datetime.strptime(time_str,'%I:%M %p')
            time_var_end = time_var + timedelta(minutes=150)
            if time_var_end.hour == 12 or time_var_end.hour == 1 or time_var_end.hour == 2:
                time_str_end = "11:59 pm"
            else:
                time_str_end = str(time_var_end.strftime("%I:%M %p"))
    #        if time_var_end >
            if channel != "NBALP":
                yield {
                    'Subject': heading,
                    'Start Date': dt_var,
                    'End Date': dt_var,
                    'Start Time': time_str,
                    'End Time' : time_str_end,
                    'All Day Event': False,
                    'Location' : channel,
                }
