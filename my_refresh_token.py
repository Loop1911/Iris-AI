from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up the OAuth2 flow
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json',  # Replace with your own client secret file
    scopes=['https://www.googleapis.com/auth/calendar']
)

# Start the OAuth2 flow
creds = flow.run_local_server(port=0)

# Print the refresh token
print("your refresh token is " + creds.refresh_token)
