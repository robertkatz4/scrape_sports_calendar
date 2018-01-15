from nba17_18 import nba_ntl_17_18
from gcal_nba_ntv import sports_insert_matches
from gcal_nba_ntv import get_calendar_events
from gcal_nba_ntv import get_credentials
from gcal_nba_ntv import sports_delete_events

sports_cal_id = 'vkuae4kj45qoo09m53l9sua280@group.calendar.google.com'
nba_list = nba_ntl_17_18()
print(nba_list[1])
sports_delete_events('vkuae4kj45qoo09m53l9sua280@group.calendar.google.com', nba_list[0])
sports_insert_matches(sports_cal_id, nba_list[1])
