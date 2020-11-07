import os.path
import re
import csv
#import pathlib

from tracks import *
from pathlib import Path

ext = ('.mp3', '.wav', '.flac', '.aac', '.ogg')
# create list of dictionaries
# create objects

class Playlist:
    def __init__(self, pl_file):
        self.name = os.path.splitext(pl_file)[0]
        self.pl_file = pl_file
        self.audio_lines = []
        self.playlist = []
        self.objs = []
        #self.tracklist = Track.objects()

    def create_audio_lines(self):
        # list of raw lines
        with open(self.pl_file) as input_file:
            self.audio_lines = [line for line in input_file.read().splitlines() if line.endswith(ext)]
        return 

    def cleanup_path(self):
        # remove header in path
        for idx, line in enumerate(self.audio_lines):
            self.audio_lines[idx] = line.replace('primary/Music/PowerAmpP/', '')
            self.audio_lines[idx] = os.path.splitext(self.audio_lines[idx])[0]
        return 


    def create_playlist(self):
        # list of dictionaries of track details
        for line in self.audio_lines:
            track_dict = {'folder' : '', 'artist' : '', 'album' : '', 'title' : ''}
            path, title = os.path.split(line)
            track_dict['title'] = title
            track_dict['folder'] = path
            regex = r"^(.*)\s-\s(.*)"
            #regex = "^(.*)?-(.*)"
            matches = re.match(regex, path)
            if matches != None:
                track_dict['artist'] = matches.group(1)
                track_dict['album'] = matches.group(2)
            else:
                #print("{}*****FIX THIS*****".format(track_dict['folder']))
                track_dict['artist'] = "unknown"
                track_dict['album'] = "unknown"
            self.playlist.append(track_dict)
        return

    def create_tracks(self):
        qty = len(self.playlist)
        for int in range(qty):
            self.objs.append(Track(self.playlist[int]['folder'], self.playlist[int]['artist'], self.playlist[int]['album'], self.playlist[int]['title']))

    def list_tracks(self):
        qty = len(self.playlist)
        print(qty)
        for int in range(qty):
            print("{}. {} ".format(int, self.objs[int]))

    def save(self):
        csv_name = "{}.csv".format(self.name)
        path = Path.cwd() / 'data' / csv_name

        with open(path.absolute(), mode='w') as csv_file:
            playlist_csv = csv.writer(csv_file, delimiter=',')
            for v in self.objs:
                playlist_csv.writerow([v.artist, v.album, v.title])
