# Author: Robert Katz
# Version: 0.2, python 2.7.13
#  This scrapes the NBA national TV schedule from
# the NBA website - NOT a scrapy project like the first iteration - hits an
# API with a curl command and outputs a CSV for direct upload into a
# Google Calendar.

import json
from datetime import datetime, timedelta


def nba_ntl_17_18():
    url = 'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2017/league/'
    file = '00_full_schedule_week.json'
    url_complete = url + file
    response = urllib.request.urlopen(url_complete)
    r = json.load(response)
    output_list = []
    for i in r['lscd']:
        for j in i['mscd']['g']:
            tv = j['bd']['b']
            for c in tv:
                s_time = datetime.strptime(j['etm'], '%Y-%m-%dT%H:%M:%S')
                if c['scope'] == 'natl' and c['type'] == 'tv' \
                        and c['disp'] != 'NBA TV' \
                        and s_time > datetime(2017, 10, 16):
                    subject = j['v']['tc'] + ' ' + '@' + ' ' + j['h']['tc']
                    e_time = s_time + timedelta(hours=2, minutes=30)
                    if e_time.hour < 10:
                        e_time = s_time.replace(hour=23, minute=59)
                    timezone = 'America/New_York'
                    output = dict([('summary', subject),
                                   ('description', 'NBA National TV schedule'),
                                   ('start', {}),
                                   ('end', {}),
                                   ('location', c['disp']),
                                   ('All Day Event', False)])
                    output['start']['dateTime'] = '{:%Y-%m-%dT%H:%M:%S}'.format(s_time)
                    output['start']['timeZone'] = timezone
                    output['end']['dateTime'] = '{:%Y-%m-%dT%H:%M:%S}'.format(e_time)
                    output['end']['timeZone'] = timezone
                    output_list.append(output)
    return output_list


def knicks_17_18():
    url = 'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2017/league/'
    file = '00_full_schedule_week.json'
    url_complete = url + file
    response = urllib.request.urlopen(url_complete)
    r = json.load(response)
    output_list = []
    for i in r['lscd']:
        for j in i['mscd']['g']:
            tv = j['bd']['b']
            for c in tv:
                s_time = datetime.strptime(j['etm'], '%Y-%m-%dT%H:%M:%S')
                if (c['scope'] == 'home' and c['type'] == 'tv' or \
                    c['scope'] == 'away' and c['type'] == 'tv') \
                        and s_time > datetime(2017, 10, 16) \
                        and 'NYK' in j['gcode']:
                    subject = j['v']['tc'] + ' ' + '@' + ' ' + j['h']['tc']
                    e_time = s_time + timedelta(hours=2, minutes=30)
                    if e_time.hour < 10:
                        e_time = s_time.replace(hour=23, minute=59)
                    timezone = 'America/New_York'
                    output = dict([('summary', subject),
                                   ('description', 'Knicks schedule'),
                                   ('start', {}),
                                   ('end', {}),
                                   ('location', c['disp']),
                                   ('All Day Event', False)])
                    output['start']['dateTime'] = '{:%Y-%m-%dT%H:%M:%S}'.format(s_time)
                    output['start']['timeZone'] = timezone
                    output['end']['dateTime'] = '{:%Y-%m-%dT%H:%M:%S}'.format(e_time)
                    output['end']['timeZone'] = timezone
                    output_list.append(output)
    return output_list


if __name__ == "__main__":
    knicks_17_18()
