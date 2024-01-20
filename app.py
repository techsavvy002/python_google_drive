import os
import csv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

# Function to create a Drive service using service account
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
def create_service():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'credentials.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    return build('drive', 'v3', credentials=credentials)

# Function to list files in a given folder
def list_files(service, folder_id):
    results = service.files().list(q=f"'{folder_id}' in parents", 
                                   fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items

# Function to get file download link
def get_download_link(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# Your folder's URL (make sure the folder is shared with the service account)
folder_url = config['drive_folder_url']
folder_id = folder_url.split("/")[-1]

# Create a service
service = create_service()

# List files in the folder
files = list_files(service, folder_id)

# Extract download URLs and filenames
data = [(file['name'], get_download_link(file['id'])) for file in files if file['name'].lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]

# Save as CSV
with open('drive_images.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['File Name', 'IMage SRC'])
    writer.writerows(data)

print("CSV file created with image URLs and filenames.")