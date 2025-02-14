import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv
from datetime import datetime 

# Define the base directory for file paths
load_dotenv()
BASE_DIR = os.getenv('BASE_DIR')
os.makedirs(BASE_DIR, exist_ok=True)

# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def authenticate_google_account():
    creds = None
    token_path = os.path.join(BASE_DIR, 'token.json')
    credentials_path = os.path.join(BASE_DIR, 'credentials.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds

def main():
    creds = authenticate_google_account()
    print("Authorization successful. The token.json file has been created.")
    print(f"02_google_auth ran at {datetime.now()}")
    print("#-------------------------------------------------#")

if __name__ == '__main__':
    main()
