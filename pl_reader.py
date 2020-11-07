import pandas as pd

from spotify_client import *
from pl_format import *
#from dbcontrol.py import *

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
#print(*pl.audio_lines, sep = '\n')

pl.create_playlist()
#print(*pl.playlist, sep = '\n')

pl.create_tracks()

#pl.list_tracks()

# for v in enumerate(pl.objs):
#     print(pl.objs[v]['album'])

# print(pl.objs[1].album)
# print(pl.playlist[0]['artist'])

pl.save()

# for k, v in enumerate(pl.objs):
#     print(v.artist, v.album, v.title)

# for k,v in enumerate(pl.playlist):
#     print(pl.playlist[k]["artist"])