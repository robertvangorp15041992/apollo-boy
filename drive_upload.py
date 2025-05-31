# drive_upload.py
from google.oauth2 import service_account
from googleapiclient.discovery import build
import mimetypes

def upload_to_drive(file_path, folder_id=None):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_file(
        'credentials.json', scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': file_path.split("/")[-1],
        'parents': [folder_id] if folder_id else []
    }

    media_mime_type = mimetypes.guess_type(file_path)[0]
    media = {
        'mimeType': media_mime_type,
        'body': open(file_path, 'rb')
    }

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"✅ Uploaded to Google Drive, File ID: {file.get('id')}")
