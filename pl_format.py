import os.path

ext = ('.mp3', '.wav', '.flac', '.aac', '.ogg')
# create list of dictionaries
# create objects

class Playlist:
    def __init__(self, pl_file):
        self.name = os.path.splitext(pl_file)[0]
        self.pl_file = pl_file
    
    def create_audio_lines(self):
        # list of raw lines
        with open(self.pl_file) as input_file:
            audio_lines = [line for line in input_file.read().splitlines() if line.endswith(ext)]
        print(*audio_lines, sep = "\n") 
        return audio_lines

    def create_playlist(self):
        pass