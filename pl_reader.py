import os.path
import pandas as pd
import re
from psycopg2 import OperationalError
# Script to open m3u8 files and pull folder name and title
# Folder name (Artist - Album) then needs to get split into Artist / Album
# Artist, Album, Title should all be entered into sql DB
# Any folders that don't have "-", get flagged for edits in sql
ext = ('.mp3', '.wav', '.flac', '.aac', '.ogg')

# READ USER INPUT SPECIFIED FILE AND ASSIGN LINES THAT END WITH AUDIO EXTENSION INTO audio_lines ARRAY

class Track:
    def __init__(self, folder, artist, album, title):
        self.folder = folder
        self.artist = artist
        self.album = album
        self.title = title    #strip ext and track number
        print(self.artist + " - " + self.album + " - " + self.title)

    def __str__(self):
            return 'aowiejfoiajwoeifjaoiwejfoiawjef{} - {} - {}'.format(self.artist, self.album, self.title)



file_name = input("Enter the full file path for the m3u8 file you wish to create an SQL DB:  \n> ")
with open(file_name) as input_file:
    playlist_byline = input_file.read().splitlines()
    audio_lines = []

for line in playlist_byline:
    if line.endswith(ext):
        audio_lines.append(line)

#print(audio_lines)
print(*audio_lines, sep = "\n") 

playlist = []
for line in audio_lines:
    track_dict = {'Folder' : '', 'Artist' : '', 'Album' : '', 'Title' : ''}
    path, title = os.path.split(line)
    path_short = path.replace('primary/Music/PowerAmpP/', '')
#   file, playlist[i] = track_dict.update({'Title' : file})
    track_dict['Folder'] = path_short
    #re.split(r'[-]*',short_path)
    regex = r"^(.*)\s-\s(.*)"

    test_str = path_short

    #matches = re.finditer(regex, test_str)

    # for matchNum, match in enumerate(matches):
    #     for groupNum in range(0, len(match.groups())):
    #         groupNum = groupNum + 1
    #         print ("Group {groupNum}: {group}".format(groupNum = groupNum, group = match.group(groupNum)))
    # track_dict['Artist'] = match.group(1)
    # track_dict['Album'] = match.group(2)
    #===========================================================================
    matches = re.match(regex, test_str)
    if matches != None:
        track_dict['Artist'] = matches.group(1)
        track_dict['Album'] = matches.group(2)
    else:
        track_dict['Artist'] = "unknown"
        track_dict['Album'] = "unknown"
    #print("testgroup2 =" m.group(1))
    #track_dict['Artist'] = match.group(1)
    #track_dict['Album'] = match.group(2)
    
    track_dict['Title'] = title
    playlist.append(track_dict)

## Populates playlist_dict with key = folder, values = list of files
#    if path_short in playlist_dict:
#        playlist_dict[path_short].append(file)
#    else:
#        playlist_dict[path_short] = [file]


#print(track_dict)
print("________________________________")
print(playlist)

print(*playlist, sep = "\n")

# 
#pd.set_option('display.max_colwidth', None)
#playlist_df = pd.DataFrame(playlist_dict.items(), columns = ["Folder", "Track"])
# SPLIT ARTIST FROM ALBUM
#playlist_df[['Artist', 'Album']] = playlist_df.Folder.str.split("-", expand = True)
#print(playlist_df)

# create list of objects using class Track
tracks = []
qty = len(playlist)
print(qty)    #86
for i in range(1,qty):
    tracks.append("Track" + str(i))
print(tracks)

for idx, val in enumerate(tracks):
    val = Track(playlist[idx]['Folder'], playlist[idx]['Artist'], playlist[idx]['Album'], playlist[idx]['Title'])
    #print(idx, val.folder)

#test = playlist[0]['Folder']
# test = track73.getattr()
print(type(tracks[6]))
thetrack = Track('FOLDER', 'ARTIST', 'ALBUM', 'TITLE')
print(getattr(thetrack, 'folder'))
print(type(thetrack))

#objs = [Track() for i in range(qty)]


objs = list()
for idx in range(qty):
    objs.append(Track(playlist[idx]['Folder'], playlist[idx]['Artist'], playlist[idx]['Album'], playlist[idx]['Title']))
print(objs)


for obj in objs:
    print(obj)


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycop2.connect(
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

    