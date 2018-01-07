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

import json, urllib2
from datetime import datetime, timedelta, date
from csv import DictWriter

url = 'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2017/league/00_full_schedule_week.json'
response = urllib2.urlopen(url)
r = json.load(response)
output_list = []
for i in r['lscd']:
    for j in i['mscd']['g']:
        tv = j['bd']['b']
        for c in tv:
            s_time = datetime.strptime(j['etm'], '%Y-%m-%dT%H:%M:%S')
            if c['scope'] == 'natl' and s_time > datetime(2017, 10, 16):
                subject = j['v']['tc'] + ' ' + '@' + ' ' + j['h']['tc']
                e_time = s_time + timedelta(hours=2, minutes=30)
                if e_time.hour < 10:
                    e_time = s_time.replace(hour=23,minute=59)
                output = dict([('Subject', subject), \
                ('Start Date', '{:%m/%d/%y}'.format(s_time)),\
                ('Start Time', '{:%H:%M}'.format(s_time)),\
                ('End Date', '{:%m/%d/%y}'.format(e_time)),\
                ('End Time', '{:%H:%M}'.format(e_time)),\
                ('Location', c['disp']),\
                ('All Day Event', False)])
                output_list.append(output)
                break

keys = output_list[0].keys()
with open('nba_2017.csv', 'wb') as output_file:
    dict_writer = DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(output_list)



#            print k
#    print a['bd']['b'][0]['disp'],a['bd']['b'][0]['scope']