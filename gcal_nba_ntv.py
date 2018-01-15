from __future__ import print_function
import httplib2
import os
from sys import exit

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime import datetime

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


def list_calendars(service, verbose=True):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        if verbose is True:
            for calendar_list_entry in calendar_list['items']:
                print (calendar_list_entry['summary'])
                print (calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break


def get_calendar_events(service, gcal_id, dates):
    """Pulls list of events on a calendar
    Returns json of all event attributes
    """
    eventsResult = service.events().list(
        calendarId=gcal_id,
        timeMin=dates['begin'], maxResults=600, singleEvents=True,
        orderBy='startTime').execute()
    matches = eventsResult.get('items', [])
    if not matches:
        print('No upcoming events found.')
    return matches


def sports_delete_events(icalendar, schedule_name, schedule_dict, verbose=True):
    """
    Takes calendar, NEEDS BESPOKE FILTER IN filter_events_schedule to find
    event IDs to be deleted, and deletes those ids
    from the given calendar.
    """

    service = get_credentials()
    print('Retriving matches from the '
          + schedule_name + ' schedule')
    icalendar_json_list = get_calendar_events(service, icalendar, schedule_dict)
    if schedule_name == 'nba':
        list_matches = tuple((x['id'], x['summary'])
                             for x in icalendar_json_list
                             if x['description'] == 'NBA National TV schedule')
    elif schedule_name == 'nyk':
        list_matches = tuple((x['id'], x['summary'])
                             for x in icalendar_json_list
                             if x['description'] == 'Knicks schedule')
    else:
        exit('No schedule specified')
    print('Retrived ' + str(len(list_matches)) + ' matches ' +
          'from the ' + schedule_name + ' schedule, deleting...')
    for i, s in list_matches:
        if verbose is True:
            print(s)
        service.events().delete(calendarId=icalendar, eventId=i).execute()
    print('Deleted ' + str(len(list_matches)) + ' events from the ' +
          schedule_name + ' schedule with the appropriate filter')


def sports_insert_matches(gcal_id, schedule):
    """
    Takes a Google Calendar API service object, and a list of dict objects,
    inserts into gCal
    """
    service = get_credentials()
    for m in schedule:
        event = service.events().insert(calendarId=gcal_id, body=m).execute()
        print(m['summary'], m['start']['dateTime'])
