from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE = Path(__file__).resolve().parent
CREDENTIALS = BASE / "credentials.json"
TOKEN = BASE / "token.json"

def main():
    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN.write_text(creds.to_json(), encoding="utf-8")

    svc = build("gmail", "v1", credentials=creds)
    profile = svc.users().getProfile(userId="me").execute()
    print("OK. Gmail profile:")
    print("  email:", profile.get("emailAddress"))
    print("  messagesTotal:", profile.get("messagesTotal"))
    print("  threadsTotal:", profile.get("threadsTotal"))

if __name__ == "__main__":
    main()
