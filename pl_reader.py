import os.path
import pandas as pd
# Script to open m3u8 files and pull folder name and title
# Folder name (Artist - Album) then needs to get split into Artist / Album
# Artist, Album, Title should all be entered into sql DB
# Any folders that don't have "-", get flagged for edits in sql
ext = ('.mp3', '.wav', '.flac', '.aac', '.ogg')

# READ USER INPUT SPECIFIED FILE AND ASSIGN LINES THAT END WITH AUDIO EXTENSION INTO audio_lines ARRAY
file_name = input("Enter the full file path for the m3u8 file you wish to create an SQL DB:  \n> ")
with open(file_name) as input_file:
    playlist_byline = input_file.read().splitlines()
    audio_lines = []

for line in playlist_byline:
    if line.endswith(ext):
        audio_lines.append(line)

# CREATE playlist_dict WITH KEY:VALUE AS artist/album:track 
playlist_dict = {}
for i in audio_lines:
    path, file = os.path.split(i)
    path_short = path.replace('primary/Music/PowerAmpP/', '')

    if path_short in playlist_dict:
        playlist_dict[path_short].append(file)
    else:
        playlist_dict[path_short] = [file]



# 
pd.set_option('display.max_colwidth', None)
playlist_df = pd.DataFrame(playlist_dict.items(), columns = ["Folder", "Track"])

# SPLIT ARTIST FROM ALBUM
playlist_df[['Artist', 'Album']] = playlist_df.Folder.str.split("-", expand = True)

print("________________________________")
print(playlist_df)



### Breaks up artist-album into folder and subfolders if CD1.. exists
# folders = []      
# print(folders)
# while 1:
#     path_short, folder = os.path.split(path)
#     print(f"while loop path: " + path_short)
#     print(f"while loop folder: " + folder)
#     print(folders)
#     if folder != ("" or "PowerAmpP" or "Music" or "primary"):
#         folders.append(folder)
#     break   
# folders.reverse()
# print(folders)
# print(file)



    ## Add y/z.mp3 into SQL DB as y = folder, z = filename
    ## split y into columns 'artist' and 'album' based on '-' character.  if no '-', do nothing.

