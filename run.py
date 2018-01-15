from datetime import datetime

from nba17_18 import nba_ntl_17_18
from gcal_nba_ntv import sports_insert_matches
from gcal_nba_ntv import sports_delete_events

sports_cal_id = 'vkuae4kj45qoo09m53l9sua280@group.calendar.google.com'

schedule_begin_end = {}
schedule_begin_end['nba'] = {}
schedule_begin_end['nba']['begin'] = \
        datetime(2017, 10, 16, 12, 00, 00).isoformat() + 'Z'
schedule_begin_end['nba']['end'] = \
        datetime(2018, 04, 12, 12, 00, 00).isoformat() + 'Z'
schedule_begin_end['nba']['matches'] = nba_ntl_17_18()

for schedule_name, schedule_values in schedule_begin_end.iteritems():
    sports_delete_events(sports_cal_id,
                         schedule_name,
                         schedule_values)
    print('Inserting ' + str(len(schedule_values['matches'])) +
          ' matches from ' + schedule_name + ' schedule')
    sports_insert_matches(sports_cal_id, schedule_values['matches'])
