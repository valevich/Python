#!/usr/bin/env python

from __future__ import print_function
from googleapiclient import errors
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import os
from shutil import copyfile
path2 = os.path.abspath('credentials.json')
path3 = os.path.abspath('token.json')
path = "/users/henryvalevich/Downloads/Temp Current/"

from datetime import datetime
print ("=====================  START  =====================")
now = datetime.now() # current date and time
date_time = now.strftime("%m%d%Y")
retval = os.getcwd()
print ("Current working directory %s" % retval)
os.chdir( path )
retval = os.getcwd()
print ("Directory changed successfully %s" % retval)

os.system('clear')



def get_authenticated(SCOPES, credential_file=path2,
                  token_file=path3, service_name='drive',
                  api_version='v3'):
    store = file.Storage(token_file)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credential_file, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build(service_name, api_version, http=creds.authorize(Http()))
    return service


def retrieve_all_files(service):

    result = []
    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(**param).execute()

            result.extend(files['files'])
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            break

    return result


def insert_file(service, name, description, parent_id, mime_type, filename):

    media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
    body = {
        'name': name,
        'description': description,
        'mimeType': mime_type
    }
    # Set the parent folder.
    if parent_id:
        body['parents'] = [{'id': parent_id}]

    try:
        file = service.files().create(
            body=body,
            media_body=media_body).execute()

        # Uncomment the following line to print the File ID
        #print ('File ID: %s' % file['id'])

        return file
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'


def update_file(service, file_id, new_name, new_description, new_mime_type,
            new_filename):

    playlistpath = "/Users/henryvalevich/odrive/DOWNLOADS_Box_25G_valevich@aol.com/Downloads/IPTV/Playlists/4hometv10/"
    
    try:
        file = service.files().get(fileId=file_id).execute()

        del file['id']      
        media_body = MediaFileUpload(
            playlistpath+new_filename, mimetype=new_mime_type, resumable=True)

        updated_file = service.files().update(
            fileId=file_id,
            body=file,
            media_body=media_body).execute()
        return updated_file
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None


def update_main():
    
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: (UPDATE GOOGLE DRIVE) ~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    playlistpath = "/Users/henryvalevich/odrive/DOWNLOADS_Box_25G_valevich@aol.com/Downloads/IPTV/Playlists/4hometv10/"
    fno = 0

    service = get_authenticated(SCOPES)
    service.about().get(fields = "user, storageQuota").execute()
    results = retrieve_all_files(service)

    for filename in sorted(os.listdir(playlistpath)):
    
        if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
#            print ("File to Upload: " + filename)
            fno += 1
            target_file_descr = 'Description of ' + filename
            target_file = filename
            target_file_name = target_file
            target_file_id = [file['id'] for file in results if file['name'] == target_file_name]

            if len(target_file_id) == 0:
                print('No file called %s found in root. Create it:' % target_file_name)
                file_uploaded = insert_file(service, target_file_name, target_file_descr, None,
                                        'text/x-script.phyton', target_file_name)
            else:
                print('--- %s found. Uploading!' % target_file_name)
                file_uploaded = update_file(service, target_file_id[0], target_file_name, target_file_descr,
                                        'text/x-script.phyton', target_file_name)


    print ("---------------------------")
    print ("Total Files: " + str(fno))
    print ("---------------------------")
    print ("")



def merge4HomeTV_function():

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(merge4HomeTV_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    playlistpath = "/Users/henryvalevich/odrive/DOWNLOADS_Box_25G_valevich@aol.com/Downloads/IPTV/Playlists/4hometv10/"
    sourcepath = "/Users/henryvalevich/odrive/DOWNLOADS_Box_25G_valevich@aol.com/Downloads/IPTV/Playlists/4hometv10/Edem Source/"
    backuppath = "/Users/henryvalevich/odrive/DOWNLOADS_Box_25G_valevich@aol.com/Downloads/IPTV/Playlists/4hometv10/Backup/"

    #concat2 = open("output.m3u").read()

    files = os.listdir(path)
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    if 'Dead' in files:
        files.remove('Dead')
    if 'Backup' in files:
        files.remove('Backup')
    for idx, infile in enumerate(sorted(files)):
        print ("File #" + str(idx + 1) + "  " + infile)
    concat = ''.join([open(path + f,encoding="ISO-8859-1").read() for f in sorted(files)])
    print ("----------------------------------------") 

    for filename in sorted(os.listdir(sourcepath)):

        if filename.endswith(".m3u") or filename.endswith(".m3u8"):

            print ("Creating File: " + filename)
            with open(sourcepath + filename, 'r',encoding="ISO-8859-1") as searchfile:

                concat2 = open(sourcepath + filename).read()
                with open(playlistpath + filename, "w") as fo:
                    fo.write(concat2 + concat)

                str_idx = int(filename.find("."))
                newname = (date_time + "_" + filename[:str_idx] + ".m3u")
                copyfile(playlistpath + filename, backuppath + newname)

                

    print ("")



if __name__ == '__main__':

    merge4HomeTV_function()
    
    update_main()
    
    
