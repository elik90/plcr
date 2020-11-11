import pandas as pd

from spotify_client import *
from pl_format import *
from dbcontrol import *

# Script to open m3u8 files and organize by folder, artist, album, title
# Built using Python 3.8 & PostgreSQL 13
# OO, Dict, Nested List
# Improvements: 
# - Pull object attributes individually
# - Use SQL to create DB given any form of data (OO, list of dictionaries, pandas df)
# - Pandas Dataframe
# - strip ext and track number

# Accept user input m3u8 file and list strings with audio file extentions in audio_lines list


### user supplies directory of playlist files.  menu lists options for user to choose.
file_name = input("Enter the full file path for the m3u8 file you wish to create an SQL DB:  \n> ")
pl = Playlist(file_name)

pl.create_audio_lines()
pl.cleanup_path()
pl.create_playlist()
pl.create_tracks()
pl.save()

# Connect to default database
default_connection()
connection = connection_playlist()
cleanup_tables()
create_table_playlist_names()
create_table_tracks()

# populate 'tracks' table 
for trackdict in pl.playlist:
    columns = ', '.join(str(x).replace('/','_').replace('\'','') for x in trackdict.keys())
    values = ', '.join("'" + str(x).replace('/', '_').replace('\'','') + "'" for x in trackdict.values())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('Tracks', columns, values)
    execute_query(connection, sql)

# populate 'playlist_names' table
sql = "INSERT INTO Playlist_Names (name) VALUES (\'%s\')" % (pl.name)
execute_query(connection, sql)

# set foreign key for tracks playlist_id to 'playlist_names' (id)
sql = """
UPDATE tracks
SET playlist_id = 1
"""
execute_query(connection, sql)

# close pgsql connection
connection.close()