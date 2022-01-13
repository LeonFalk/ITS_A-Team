# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 10:49:56 2021

@author: Leon
"""

    ### Python imports to bring in library functionality
    # Google Drive Integration
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
#pip install OAuth2Client
#pip install httplib2
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

global DRIVE_Service
global folder_id

    # Watchdog Integration
#pip install watchdog
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

    # Integration Datum/Uhrzeit
from datetime import datetime as DateTime

######## Google Drive Funktionen ##############################################
        
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
        
        global DRIVE_Service
        DRIVE_Service = discovery.build('drive', 'v3', http=creds.authorize(Http()))
        return DRIVE_Service

###     Erstellt einen Ordner im abgefragten Ordner 
###     Parameter:
###         DRIVE_Service (global)
###         Ordnernamen (z.B. 'Records', Datum, Uhrzeit)
def DRIVE_create_folder(Ordnername):
    
    ###     Ordner wird im Hauptverzeichnis erstellt 'root'
    folder_id_create_folder = 'root'
    
    file_metadata = {
        'name': Ordnername,
        'parents': [folder_id_create_folder],
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = DRIVE_Service.files().create(body=file_metadata,
                                    fields='id').execute()
    
    ###     Für Testzwecke kann die Folder ID ausgegeben werden
    #print('Folder ID: %s' % file.get('id'))
    
    ###     return der ID des neu erstellten Ordners
    global folder_id
    folder_id = str(file.get('id'))
    return folder_id

###     Lädt eine Datei in die Cloud hoch
###     Parameter:
###         folder_id (global) - Speicherort Cloud
###         mimeType        - Dateityp  (String!: z.B. 'audio/wav', 'text/plain')
###         file_name       - Dateiname (String!: z.B. 'Record_2022_01_08_....')
###         file_location   - Dateiort  (String!: z.B. 'files/Testdokument.txt')
def DRIVE_create_upload(mimetype, file_name, file_location):
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
def DRIVE_print_list_of_files():        
        files = DRIVE_Service.files().list().execute().get('files', [])
        for f in files:
            print(f['name'], f['mimeType'], f['kind'])

######## Watchdog Funktionen ##################################################
    
###     Event Definitionen -> Was passiert, wenn ein Event eintritt?
def on_created(event):
    print(f"hey, {event.src_path} has been created!")
    
    ### Name muss noch extrahier werden aus {event.src_path}
    file_location = str(event.src_path)
    print('file_location: ', file_location)
    
    file_name = file_location.split("/")
    file_name = file_name[len(file_name)-1]
    
    file_type = file_name.split(".")
    file_type = file_type[len(file_type)-1]
    
    if file_type == 'txt':
        mimetype = 'text/plain'
    elif file_type == 'wav':
        mimetype = 'audio/wav'
    else:
        mimetype = 'application/octet-stream'
    print('Mimetype: ', mimetype, 'file_name: ', file_name, 'file_location: ', file_location)
    
    DRIVE_create_upload(mimetype, file_name, file_location)
    
    
def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")
    
def on_modified(event):    
    print(f"hey buddy, {event.src_path} has been modified")
    
def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")  
    
    
  
######## main Funktionen ######################################################

        ### WatchDog
def start_WatchDog():
    ###     Event Handler
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved
    
    ###     Observer
    path = "./files/"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    
    ### Start Observer
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
        
def main():
        ### 1. Drive Authentifizierung und erstellen von DRIVE_Service (global)
        ### Überprüfung fehlt noch ;)
    DRIVE_create_authentication()
    print('Authentifizierung erfolgreich: \t')
    print(DRIVE_Service)

        ### 2. Neuen Ordner erstellen und erstellen von folder_id (global)
        ### Integration der Zeitstamps etc 
    now = DateTime.now()    
    date_time = now.strftime("%d-%m-%Y_%H-%M")
    Ordnername = "Record_" + date_time
    
    DRIVE_create_folder(Ordnername)
    print('Ordner: ', Ordnername, 'erstellt, mit der ID: ', folder_id)
    
        ### 2. WatchDog starten
    print('Ab hier läuft der Watchdog...')
    start_WatchDog()

######## Funktionsaufruf ######################################################
main()