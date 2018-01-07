# Author: Robert Katz
# Version: 0.2, python 2.7.13
# Program description: Scrapy. This scrapes the NBA national TV schedule from
# the NBA website - NOT a scrapy project like the first iteration - hits an
# API with a curl command and outputs a CSV for direct upload into a
# Google Calendar.
# output: csv
# Revision history:

import json
from urllib2 import urlopen
from datetime import datetime, timedelta
from csv import DictWriter

url = 'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2017/league/'
file = '00_full_schedule_week.json'
url_complete = url + file
response = urlopen(url_complete)
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
                    e_time = s_time.replace(hour=23, minute=59)
                output = dict([('Subject', subject),
                               ('Start Date', '{:%m/%d/%y}'.format(s_time)),
                               ('Start Time', '{:%H:%M}'.format(s_time)),
                               ('End Date', '{:%m/%d/%y}'.format(e_time)),
                               ('End Time', '{:%H:%M}'.format(e_time)),
                               ('Location', c['disp']),
                               ('All Day Event', False)])
                output_list.append(output)
                break

keys = output_list[0].keys()
with open('nba_17_18.csv', 'wb') as output_file:
    dict_writer = DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(output_list)
