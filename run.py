from datetime import datetime

from nba17_18 import nba_ntl_17_18
from nba17_18 import knicks_17_18
from gcal_nba_ntv import sports_insert_matches
from gcal_nba_ntv import sports_delete_events

sports_cal_id = 'vkuae4kj45qoo09m53l9sua280@group.calendar.google.com'
nba_ntl_cal_id = 'snoof255d4acqjlhh9aogk3l5o@group.calendar.google.com'

schedule_begin_end = {}
schedule_begin_end['nba'] = {}
schedule_begin_end['nba']['begin'] = \
        datetime(2017, 10, 16, 12, 00, 00).isoformat() + 'Z'
schedule_begin_end['nba']['end'] = \
        datetime(2018, 04, 12, 12, 00, 00).isoformat() + 'Z'
schedule_begin_end['nba']['matches'] = nba_ntl_17_18()
# schedule_begin_end['nyk'] = {}
# schedule_begin_end['nyk']['begin'] = \
#         datetime(2017, 10, 16, 12, 00, 00).isoformat() + 'Z'
# schedule_begin_end['nyk']['end'] = \
#         datetime(2018, 04, 12, 12, 00, 00).isoformat() + 'Z'
# schedule_begin_end['nyk']['matches'] = knicks_17_18()

cal_list = [nba_ntl_cal_id]

for i in cal_list:
    for schedule_name, schedule_values in schedule_begin_end.iteritems():
        sports_delete_events(i,
                             schedule_name,
                             schedule_values)
        print('Inserting ' + str(len(schedule_values['matches'])) +
              ' matches from ' + schedule_name + ' schedule')
        sports_insert_matches(i, schedule_values['matches'])
