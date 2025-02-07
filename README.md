# Calendar App 

## Prerequisites 

## Steps to Set Up OAuth2 Credentials and Download credentials.json
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


## To run the files:

The following files should be run: 
- scripts/shell.rtf
This will automatically fetch all the data for the past 1 week from your calendars and save it in a csv file. 


