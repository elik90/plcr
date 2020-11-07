import os.path
import re

from tracks import *

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
                print("{}*****FIX THIS*****".format(track_dict['folder']))
                track_dict['artist'] = "unknown"
                track_dict['album'] = "unknown"
            self.playlist.append(track_dict)
        return

    def create_tracks(self):
        qty = len(self.playlist)
        for int in range(qty):
            self.objs.append(Track(self.playlist[int]['folder'], self.playlist[int]['artist'], self.playlist[int]['album'], self.playlist[int]['title']))
            print("{}. {} ".format(int, self.objs[int]))

    # def save(self):
    #     my_path = os.path.abspath(os.path.dirname(__file__))
    #     path = os.path.join(my_path, "../data/playlist.csv")

    #     with open(path, 'w') as csvfile:
    #         playlist_csv = csv.writer(csvfile, delimiter=',')
    #         playlist_csv.writerow(['name', 'age', 'role', 'school_id', 'password'])
    #         for track in self.tracklist:
    #             playlist_csv.writerow([track.folder, track.artist, track.album, track.title])