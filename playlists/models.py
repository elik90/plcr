from django.db import models
import os.path
from pathlib import Path

# Create your models here.
class Playlist(models.Model):
    title = models.CharField(max_length=220)
    content = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)
    filename = models.FileField(upload_to='playlists/uploaded/')
    isgenerated = models.BooleanField(default=False)

    # def __init__(self):
    #     self.audio_lines = []

    def __str__(self):
        return 'title: ' + self.title + ' ' + 'filename: ' + str(self.filename)

    def generate_tracklist(self):
        ext = ('.mp3', '.wav', '.flac', '.aac', '.ogg')
        p = os.path.join(Path(__file__).parents[1], 'media')
        filepath = os.path.join(p, str(self.filename))
        with open(filepath) as input_file:
            self.audio_lines = [line for line in input_file.read().splitlines() if line.endswith(ext)]
        print(self.audio_lines)


class Track(models.Model):
    id = models.AutoField(primary_key=True)
    folder = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    def __str__(self):
        return 'track #: ' + self.id + ' ' + 'artist: ' + self.artist + ' ' + 'album: ' + self.album + ' ' + 'title: ' + self.title + ' '


