from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage. Creates a Google Calendar API service object

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential, and gcal service object
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    return service


def get_calendar_events(service, gcal_id):
    """Pulls list of events on a calendar
    Returns json of all event attributes
    """

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId=gcal_id,
        timeMin=now, maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    matches = eventsResult.get('items', [])
    if not matches:
        print('No upcoming events found.')
    return matches

def filter_events_schedule(service, json_list, verbose=True):
    """Parses list of events to pull event id for each schedule based on a
    filter in a list comprehension
    """

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    json_list_info = [x['id'] for x in json_list if ' @ ' in x['summary']]
    if verbose is True:
        json_list_summaries = [x['summary'] for x in json_list if ' @ ' in x['summary']]
        print(json_list_summaries)
    return json_list_info
    # for match in json:
    #     start = match['start'].get('dateTime', match['start'].get('date'))
    #     output = match['summary'], match['iCalUID']
    #     matches_parsed.append(output)
    # return matches_parsed


def list_calendars(service, verbose=True):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        if verbose==True:
            for calendar_list_entry in calendar_list['items']:
                print (calendar_list_entry['summary'])
                print (calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

def sports_insert_matches(service, gcal_id):
    """
    Takes a Google Calendar API service object, and a list of dict objects,
    inserts into gCal
    """
    meetings = [{
      'summary': 'Google I/O 2015',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'A chance to hear more about Google\'s developer products.',
      'start': {
        'dateTime': '2018-01-28T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2018-01-28T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
      ],
      'attendees': [
        {'email': 'lpage@example.com'},
        {'email': 'sbrin@example.com'},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    } ,
    {
      'summary': 'Google I/O 2015',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'A chance to hear more about Google\'s developer products.',
      'start': {
        'dateTime': '2018-01-29T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2018-01-29T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }
    ]
    print('Inserting event into Sports')
    for meeting in meetings:
        event = service.events().insert(calendarId=gcal_id, body=meeting).execute()

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    eventsResult = service.events().list(
        calendarId=gcal_id,
        timeMin=now, maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))


def sports_delete_events(service, icalendar, del_event_ids):
    """
    Takes list of event ids and deletes them from the given calendar.
    """
    print('deleting events')
    for i in del_event_ids:
        print('event_id for del', i)
        print('calendar for del', icalendar)
        service.events().delete(calendarId=icalendar, eventId=i).execute()


if __name__ == '__main__':
    service = get_credentials()
    sports_cal_id = 'vkuae4kj45qoo09m53l9sua280@group.calendar.google.com'
    list_calendars(service)
    # sports_insert_matches(service, gcal_id=sports_cal_id)
    calendar_events = get_calendar_events(service, sports_cal_id)
    this_schedule_iCalUIDs = filter_events_schedule('Google', service, sports_cal_id, calendar_events)
    print('all ids', this_schedule_iCalUIDs)
    sports_delete_events(service,
                         icalendar=sports_cal_id,
                         del_event_ids=this_schedule_iCalUIDs)
