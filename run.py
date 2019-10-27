from datetime import datetime

import gin

from nba17_18 import nba_ntl_17_18
from nba17_18 import knicks_17_18
from gcal_nba_ntv import sports_insert_matches
from gcal_nba_ntv import sports_delete_events

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

@gin.configurable
def main(cal=None):
    cal=cal
    cal_list = [cal]
    for i in cal_list:
        for schedule_name, schedule_values in schedule_begin_end.iteritems():
            sports_delete_events(i,
                                 schedule_name,
                                 schedule_values)
            print('Inserting ' + str(len(schedule_values['matches'])) +
                  ' matches from ' + schedule_name + ' schedule')
            sports_insert_matches(i, schedule_values['matches'])


if __name__ == "__main__":
    gin.parse_config_file('top_level_params.gin')
    main()
