import os.path
import re
import psycopg2
import csv
import pandas as pd

from psycopg2 import OperationalError
from spotify_client import *
from pl_format import *

# Script to open m3u8 files and organize by folder, artist, album, title
# Built using Python 3.8 & PostgreSQL 13
# OO, Dict, Nested List
# Improvements: 
# - Pull object attributes individually
# - Use SQL to create DB given any form of data (OO, list of dictionaries, pandas df)
# - Pandas Dataframe
# - strip ext and track number



class Track:
    def __init__(self, folder, artist, album, title):
        self.folder = folder
        self.artist = artist
        self.album = album
        self.title = title    
        #print(self.artist + " - " + self.album + " - " + self.title)

    def __str__(self):
        # Returns formatted track description
        return '{} - {} - {}'.format(self.artist, self.album, self.title)

# Accept user input m3u8 file and list strings with audio file extentions in audio_lines list
file_name = input("Enter the full file path for the m3u8 file you wish to create an SQL DB:  \n> ")
# with open(file_name) as input_file:
#     playlist_byline = input_file.read().splitlines()
#     audio_lines = []
# for line in playlist_byline:
#     if line.endswith(ext):
#         audio_lines.append(line)
# print("==========audio_lines:")
# print(*audio_lines, sep = "\n") 

asdf = Playlist(file_name)
print(asdf.name)
asdf.create_audio_lines()



# Using audio_lines, create playlist list of track dictionaries
playlist = []
for line in audio_lines:
    track_dict = {'folder' : '', 'artist' : '', 'album' : '', 'title' : ''}
    path, title = os.path.split(line)
    path_short = path.replace('primary/Music/PowerAmpP/', '')
    track_dict['title'] = title
    track_dict['folder'] = path_short
    regex = r"^(.*)\s-\s(.*)"
    #regex = "^(.*)?-(.*)"
    matches = re.match(regex, path_short)
    if matches != None:
        track_dict['artist'] = matches.group(1)
        track_dict['album'] = matches.group(2)
    else:
        print("{}*****FIX THIS*****".format(track_dict['folder']))
        track_dict['artist'] = "unknown"
        track_dict['album'] = "unknown"
        
    playlist.append(track_dict)
print("========== playlist:")
print(*playlist, sep = "\n")

# create list of objects using class Track
qty = len(playlist)
print("==========tracks:")
objs = []
for int in range(qty):
    objs.append(Track(playlist[int]['folder'], playlist[int]['artist'], playlist[int]['album'], playlist[int]['title']))
    print("{}. {} ".format(int, objs[int]))


# SQL Implementation
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occured")
    return connection

# Create new db in postgresql db server
def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def execute_db_check(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        list_database = cursor.fetchall()
        print(list_database)
        if 'playlists' in list_database:
            print("'{}' Database already exists".format("playlists"))
            return True
        else:
            print("'{}' Database does not exist.".format("playlists"))
            return False
            

    except OperationalError as e:
        print(f"The error '{e}' occurred")


# Connect to default database
connection = create_connection(
    "postgres", "postgres", "iguana90", "127.0.0.1", "5432"
)
db_check_query = ("SELECT datname FROM pg_database;")
execute_db_check(connection, db_check_query)

if execute_db_check is True:
    create_database_query = "CREATE DATABASE playlists"
    create_database(connection, create_database_query)
else:

#if db_check_query is True:

    print('Done')


# Connect to playlist database based on create_database_query above
connection = create_connection("playlists", "postgres", "iguana90", "127.0.0.1", "5432")

create_playlist_table = """
CREATE TABLE IF NOT EXISTS Tracks (
  Folder character (90),
  Artist character (90), 
  Album character (90),
  Title character (90)
)
"""
execute_query(connection, create_playlist_table)

for trackdict in playlist:
    columns = ', '.join(str(x).replace('/','_').replace('\'','') for x in trackdict.keys())
    values = ', '.join("'" + str(x).replace('/', '_').replace('\'','') + "'" for x in trackdict.values())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('Tracks', columns, values)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(sql)
