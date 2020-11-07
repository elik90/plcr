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

    # @classmethod
    # def objects(cls):
    #     tracks = []
    #     my_path = os.path.abspath(os.path.dirname(__file__))
    #     path = os.path.join(my_path, "../data/tracks.csv")


    #     with open(path) as csvfile:
    #         reader = csv.DictReader(csvfile)
    #         for row in reader:
    #             print(dict(row))
    #             tracks.append(Track(**dict(row)))
    #     return tracks

