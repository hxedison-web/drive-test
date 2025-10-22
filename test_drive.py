import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Load credentials from environment variable
creds_json = os.environ.get('GOOGLE_CREDENTIALS')
if not creds_json:
    raise Exception("GOOGLE_CREDENTIALS environment variable not set")

creds_dict = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(
    creds_dict,
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)

# Build the Drive service
service = build('drive', 'v3', credentials=credentials)

# List files in a specific folder (replace FOLDER_ID with your actual folder ID)
# FOLDER_ID = '1yQhus052FeqxppUIYqWrdXsgHV51GRo-'  #  HX Edison Google Drive announcement folder
FOLDER_ID = '1E2bzftdzCv0nxZtlst4OkhqW1P3E6Q8w'  #  HX Edison Google Drive news folder

# print(f"Listing files in folder HX Edison announcement, ID: {FOLDER_ID}...")
print(f"Listing files in folder HX Edison news, ID: {FOLDER_ID}...")

results = service.files().list(
    q=f"'{FOLDER_ID}' in parents",
    pageSize=10,
    fields="files(id, name, mimeType, modifiedTime)"
).execute()

files = results.get('files', [])

if not files:
    print('No files found.')
else:
    print('Files:')
    for file in files:
        print(f"  - {file['name']} (ID: {file['id']}, Type: {file['mimeType']})")

# Download a file example (optional)
# Create downloaded directory
os.makedirs('downloaded', exist_ok=True)

for file in files:
    # Only download actual files, not Google Docs/Sheets
    if not file['mimeType'].startswith('application/vnd.google-apps'):
        print(f"\nDownloading {file['name']}...")
        request = service.files().get_media(fileId=file['id'])
        
        file_path = os.path.join('downloaded', file['name'])
        fh = io.FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"  Download {int(status.progress() * 100)}%")
        
        print(f"  Saved to {file_path}")

print("\nTest complete!")