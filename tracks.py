import csv
import os.path
from pathlib import Path

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


