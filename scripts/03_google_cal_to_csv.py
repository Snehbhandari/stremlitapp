import os
import json
import csv
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta, timezone
from dateutil import parser
import traceback
from datetime import datetime, timedelta

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Function to authenticate and create a service object for the Google Calendar API
def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("No valid credentials. Please authenticate.")
            return None
    service = build('calendar', 'v3', credentials=creds)
    return service

def read_calendar_ids(file_path):
    with open(file_path, 'r') as file:
        calendar_ids = json.load(file)
    return calendar_ids

def get_calendar_events(service, calendar_id):
    try:
        # start_time = '2023-01-01T00:00:00Z'
        # end_time = '2025-01-01T00:00:00Z'

        # Get today's date in the required format
        end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        # Get the date one week ago
        start_time = (datetime.utcnow() - timedelta(weeks=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

        
        events_result = service.events().list(calendarId=calendar_id, timeMin=start_time, timeMax=end_time, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        
        return process_events(events)
    except Exception as e:
        print(f"An error occurred while fetching events: {e}")
        traceback.print_exc()  # Print full stack trace for debugging
        print(f"Calendar ID: {calendar_id}")
        return []

def process_events(events):
    event_data = []
    for event in events:
        start_time = event.get('start').get('dateTime') or event.get('start').get('date')
        end_time = event.get('end').get('dateTime') or event.get('end').get('date')

        try:
            start_dt = parser.parse(start_time)
            end_dt = parser.parse(end_time)
            duration_minutes = int((end_dt - start_dt).total_seconds() / 60)

            event_data.append({
                'summary': event.get('summary'),
                'start': start_dt,
                'end': end_dt,
                'duration': duration_minutes,
            })
        except Exception as e:
            print(f"Error parsing event dates: {e}")
            print(f"Start time: {start_time}, End time: {end_time}")

    return event_data

def sync_calendar_to_csv(service, calendar_ids, csv_file_path):
    all_events = []

    for calendar_name, calendar_id in calendar_ids.items():
        print(f"Fetching events for: {calendar_name}")
        events = get_calendar_events(service, calendar_id)
        if not events:
            print(f"No events found for {calendar_name}.")
            continue

        for event in events:
            event_id = event.get('id')
            event_title = event.get('summary', 'No Title')

            # Use the start and end datetimes directly
            start_dt = event['start']  # This is already a datetime object
            end_dt = event['end']      # This is also a datetime object

            # Calculate duration in minutes
            duration = int((end_dt - start_dt).total_seconds() / 60)

            # Create a row dictionary with all desired data
            row = {
                'Event ID': event_id,
                'Start Date': start_dt.date(),
                'Start Time': start_dt.time(),
                'End Date': end_dt.date(),
                'End Time': end_dt.time(),
                'Duration': duration,
                'Event Title': event_title,
                'Calendar Name': calendar_name
            }
            all_events.append(row)

    if all_events:
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Event ID', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Duration', 'Event Title', 'Calendar Name']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for event in all_events:
                writer.writerow(event)
        print(f"Calendar events have been saved to {csv_file_path}.")
    else:
        print("No events to write to CSV.")


# Main function
import os

# Main function
def main():
    service = authenticate()
    if not service:
        return
    calendar_ids = read_calendar_ids('calendars.json')

    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    # Specify the path for the CSV file
    csv_file_path = os.path.join('data', 'calendar_events.csv')
    sync_calendar_to_csv(service, calendar_ids, csv_file_path)

if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()
