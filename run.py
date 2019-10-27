from datetime import datetime

import gin

from nba17_18 import nba_ntl_tv
from gcal_nba_ntv import sports_insert_matches
from gcal_nba_ntv import sports_delete_events


def scrape_site():
    schedule_begin_end = {}
    schedule_begin_end['nba'] = {}
    schedule_begin_end['nba']['begin'] = \
            datetime(2019, 10, 16, 12).isoformat() + 'Z'
    schedule_begin_end['nba']['end'] = \
            datetime(2020, 4, 12, 12).isoformat() + 'Z'
    schedule_begin_end['nba']['matches'] = nba_ntl_tv()
    return schedule_begin_end


@gin.configurable
def main(cal=None):
    package = scrape_site()
    cal=cal
    cal_list = [cal]
    for i in cal_list:
        for schedule_name, schedule_values in package.items():
            sports_delete_events(i,
                                 schedule_name,
                                 schedule_values)
            print('Inserting ' + str(len(schedule_values['matches'])) +
                  ' matches from ' + schedule_name + ' schedule')
            sports_insert_matches(i, schedule_values['matches'])


if __name__ == "__main__":
    gin.parse_config_file('top_level_params.gin')
    main()
