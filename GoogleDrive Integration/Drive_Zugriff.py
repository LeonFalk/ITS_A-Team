# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 10:49:56 2021

@author: Leon
"""

    #1. Python imports to bring in library functionality
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

###     Erstellt Authentifizierung für die Google Drive API v3
###     und gibt Drive_Service zurück -> Authentifizierungs-Token
def create_authentication():
        ###   Obtaining application credentials
        ###   -> Zugriff auf die gesamte Drive-Struktur
        SCOPES = (
            'https://www.googleapis.com/auth/drive',                  
            )
        ###   Generiertes Token für die Authentifizierung speichern 
        ###   -> keine neue Authentifizierung nötig
        store = file.Storage('storage.json')           
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        DRIVE_Service = discovery.build('drive', 'v3', http=creds.authorize(Http()))
        return DRIVE_Service

###     Erstellt einen Ordner im abgefragten Ordner 
def create_folder(DRIVE_Service):
    folder_id = input("Parent Folder ID? ....")
    
    file_metadata = {
        'name': 'Testordner',
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = DRIVE_Service.files().create(body=file_metadata,
                                    fields='id').execute()
    print('Folder ID: %s' % file.get('id'))

###     Lädt ein .txt Dokument aus dem Ordner /files hoch in den angefragten Ordner
def create_upload(DRIVE_Service):
    ### In welchen Ordner soll hochgeladen werden? -> sonst 'root'
    folder_id = input("Parent Folder ID? ....")
    
    file_metadata = {
                    'name': 'Testdokument.txt',
                    'parents': [folder_id]
    }
    media = MediaFileUpload('files/Testdokument.txt',
                            mimetype='text/plain',
                            resumable=True)
    file = DRIVE_Service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print ('File ID: %s' % file.get('id'))

###     Zeigt alle Dateien und Ordner an -> auch die im Papierkorb..
def print_list_of_files(DRIVE_Service):        
        files = DRIVE_Service.files().list().execute().get('files', [])
        for f in files:
            print(f['name'], f['mimeType'])
            
###     MAIN        
def main():
    ### Authentifizierung aufrufen und Drive_Service erstellen
    DRIVE_Service = create_authentication()
    
    #create_folder(DRIVE_Service)
    #print_list_of_files(DRIVE_Service)
    create_upload(DRIVE_Service)
    
###     Funktionsaufruf
main()