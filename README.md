# Calendar App 

## Prerequisites 

## 1. Steps to Set Up OAuth2 Credentials and Download credentials.json
### Go to the Google Cloud Console:
- Navigate to the Google Cloud Console.
### Create a New Project or Select an Existing Project:
- Use the project selector at the top of the page to select an existing project or create a new one.
### Enable the Google Calendar API:
- Go to the "API & Services" > "Library" and search for "Google Calendar API".
- Click on the Google Calendar API and then click "Enable".
### Create OAuth 2.0 Client ID:
1.  Go to "API & Services" > "Credentials".
2. Click on "Create Credentials" and select "OAuth 2.0 Client ID".
3. You will need to configure the consent screen if you haven't done so already. This involves filling out some basic information about your application.
4. After configuring the consent screen, choose "Desktop App" as the application type.
5. Click "Create" and download the credentials.json file.

Make sure to save the file in the base directory. 
And rename the file as credentials.json 

## Download all the requirements 

## 2. To run the files:

The following files should be run to get/ update the credentials
- 01_create_id.py
- 02_google_auth.py

To get data from your calendars into a csv in your directory, run the following file 
- 03_google_cal_to_csv.py
\ This will save data from the last 1 week till the current time. 



