import os.path
import pandas as pd
import re
import psycopg2
from psycopg2 import OperationalError

# Script to open m3u8 files and organize by folder, artist, album, title
# Built using Python 3.8 & PostgreSQL 13
# OO, Dict, Nested List
# Improvements: 
# - Pull object attributes individually
# - Use SQL to create DB given any form of data (OO, list of dictionaries, pandas df)
# - Tuple and Pandas Dataframe
# - strip ext and track number

ext = ('.mp3', '.wav', '.flac', '.aac', '.ogg')

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
with open(file_name) as input_file:
    playlist_byline = input_file.read().splitlines()
    audio_lines = []
for line in playlist_byline:
    if line.endswith(ext):
        audio_lines.append(line)
print("==========audio_lines:")
print(*audio_lines, sep = "\n") 

# Using audio_lines, create playlist list of track dictionaries
playlist = []
for line in audio_lines:
    track_dict = {'Folder' : '', 'Artist' : '', 'Album' : '', 'Title' : ''}
    path, title = os.path.split(line)
    path_short = path.replace('primary/Music/PowerAmpP/', '')
    track_dict['Title'] = title
    track_dict['Folder'] = path_short
    regex = r"^(.*)\s-\s(.*)"
    #regex = "^(.*)?-(.*)"
    matches = re.match(regex, path_short)
    if matches != None:
        track_dict['Artist'] = matches.group(1)
        track_dict['Album'] = matches.group(2)
    else:
        print("{}*****FIX THIS*****".format(track_dict['Folder']))
        track_dict['Artist'] = "unknown"
        track_dict['Album'] = "unknown"
        
    playlist.append(track_dict)
print("========== playlist:")
print(*playlist, sep = "\n")

# create list of objects using class Track
qty = len(playlist)
print("==========tracks:")
objs = []
for int in range(qty):
    objs.append(Track(playlist[int]['Folder'], playlist[int]['Artist'], playlist[int]['Album'], playlist[int]['Title']))
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
    except OperationError as e:
        print(f"The error '{e}' occured")
    return connection

# Connect to default database
connection = create_connection(
    "postgres", "postgres", "iguana90", "127.0.0.1", "5432"
)

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

cur = connection.cursor()

cur.execute("SELECT datname FROM pg_database;")

list_database = cur.fetchall()

database_name = input('Enter database name to check exist or not: ')

if (database_name,) in list_database:
    print("'{}' Database already exist".format(database_name))
else:
    print("'{}' Database not exist.".format(database_name))
    create_database_query = "CREATE DATABASE playlist"
    create_database(connection, create_database_query)
connection.close()
print('Done')



# Connect to playlist database based on create_database_query above
connection = create_connection(
    "playlist", "postgres", "iguana90", "127.0.0.1", "5432"
)

create_playlist_table = """
CREATE TABLE IF NOT EXISTS Q_m3u8 (
  tracknumber integer,
  artist character (20), 
  album character (20),
  title character (20)
)
"""
execute_query(connection, create_playlist_table)


# users = [
#     ("James", 25, "male", "USA"),
#     ("Leila", 32, "female", "France"),
#     ("Brigitte", 35, "female", "England"),
#     ("Mike", 40, "male", "Denmark"),
#     ("Elizabeth", 21, "female", "Canada"),
# ]


userstest = [
    (25, "male", "USA","asdf"),
    (32, "female", "France","asdf"),
    (35, "female", "England","asdf"),
    (40, "male", "Denmark","asdf"),
    (21, "female", "Canada","asdf"),
]

user_records = ", ".join(["%s"] * len(userstest))           #?????????
insert_query = (
    f"INSERT INTO Q_m3u8 (tracknumber, artist, album, title) VALUES {user_records}"
)

connection.autocommit = True
cursor = connection.cursor()
cursor.execute(insert_query, userstest)

# clean
# separate different data organizations
# separate sql
# separate Track class
