import os
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BASE_DIR = os.getenv('BASE_DIR')

# Define the scope for Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_calendar_ids(creds):
    # Build the Google Calendar service
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API to get the list of calendars
    try:
        calendars = service.calendarList().list().execute()
        calendar_ids = {}

        for calendar in calendars.get('items', []):
            calendar_id = calendar['id']
            calendar_name = calendar['summary']
            calendar_ids[calendar_name] = calendar_id
            print(f"Calendar Name: {calendar_name}, Calendar ID: {calendar_id}")

        return calendar_ids

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    creds = None
    token_path = os.path.join(BASE_DIR, 'token.json')

    # Load credentials from token.json
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Check if the credentials are valid
    if not creds or not creds.valid:
        print("Credentials are not valid or expired.")
        return

    # Get calendar IDs
    calendar_ids = get_calendar_ids(creds)
    if calendar_ids:
        # Optionally save calendar IDs to a JSON file
        with open(os.path.join(BASE_DIR, 'calendars.json'), 'w') as f:
            json.dump(calendar_ids, f, indent=4)
        print(f"Calendar IDs have been saved to {os.path.join(BASE_DIR, 'calendars.json')}")

if __name__ == '__main__':
    main()
