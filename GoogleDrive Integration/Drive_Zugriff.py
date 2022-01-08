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
###     benötigt:
###         credentials.json (Authentifizierungsschlüssel)
###         storage.json, wenn die Authentifizierung auf dem System bereits durchgeführt wurde...
###     return:
###         Drive_Service
###         -> Authentifizierungs-Token für alle anderen Aufrufe nötig.
###     Es fehlt noch:
###     Falls Token nicht mehr aktuell/nicht erstellt ist läuft dies in einen Fehler
###         -> dies muss noch abgefangen werden!!!
def DRIVE_create_authentication():
        ###   Obtaining application credentials
        ###   in diesem Fall Zugriff auf die gesamte Drive-Struktur
        SCOPES = (
            'https://www.googleapis.com/auth/drive',                  
            )
        ###     Generiertes Token für die Authentifizierung speichern 
        ###     wenn bereits geschehen ist keine neue Authentifizierung nötig
        store = file.Storage('storage.json')           
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        DRIVE_Service = discovery.build('drive', 'v3', http=creds.authorize(Http()))
        return DRIVE_Service

###     Erstellt einen Ordner im abgefragten Ordner 
###     Parameter:
###         DRIVE_Service
###         Ordnernamen (z.B. 'Records', Datum, Uhrzeit)
def DRIVE_create_folder(DRIVE_Service, Ordnername):
    
    ###     Ordner wird im Hauptverzeichnis erstellt 'root'
    folder_id = 'root'
    
    file_metadata = {
        'name': Ordnername,
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = DRIVE_Service.files().create(body=file_metadata,
                                    fields='id').execute()
    
    ###     Für Testzwecke kann die Folder ID ausgegeben werden
    #print('Folder ID: %s' % file.get('id'))
    
    ###     return der ID des neu erstellten Ordners
    file_id = str(file.get('id'))
    return file_id

###     Lädt eine Datei in die Cloud hoch
###     Parameter:
###         folder_id       - Speicherort Cloud
###         mimeType        - Dateityp  (String!: z.B. 'audio/wav', 'text/plain')
###         file_name       - Dateiname (String!: z.B. 'Record_2022_01_08_....')
###         file_location   - Dateiort  (String!: z.B. 'files/Testdokument.txt')
def DRIVE_create_upload(DRIVE_Service, folder_id, mimetype, file_name, file_location):
    file_metadata = {
                    'name': [file_name],
                    'parents': [folder_id]
    }
    media = MediaFileUpload(file_location,
                            mimetype,
                            resumable=True)
    file = DRIVE_Service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    
    ###     return der ID der hochgeladenen Datei
    file_id = str(file.get('id'))
    return file_id

###     Zeigt alle Dateien und Ordner an. 
###     Achtung: auch die im Papierkorb..
def DRIVE_print_list_of_files(DRIVE_Service):        
        files = DRIVE_Service.files().list().execute().get('files', [])
        for f in files:
            print(f['name'], f['mimeType'], f['kind'])
  
###     MAIN        
###     - Für Testzwecke
def main():
    ### Authentifizierung aufrufen und Drive_Service erstellen
    DRIVE_Service = DRIVE_create_authentication()
    
    ### Testordner erstellen
    Ordnername = 'DiesIstNurEinTestordner'
    folder_id = DRIVE_create_folder(DRIVE_Service, Ordnername)
    
    ### Testdokument in der erstellten Testordner hochladen
    file_mimetype = 'text/plain'
    file_name = 'Record_2022_01_08_....'
    file_location = 'files/Testdokument.txt'
    DRIVE_create_upload(DRIVE_Service, folder_id, file_mimetype, file_name, file_location)
    
    ### Alle Dateien/ Ordner in der Cloud ausgeben
    #DRIVE_print_list_of_files(DRIVE_Service)
    
###     Funktionsaufruf Main()
main()
