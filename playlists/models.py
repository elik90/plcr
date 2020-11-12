from django.db import models



# Create your models here.
class Playlist(models.Model):
    #id = models.AutoField()
    title = models.CharField(max_length=220)
    content = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)
    filename = models.FileField(upload_to='playlists/uploaded/')
    #isgenerated = models.BooleanField(default=False)

    def __str__(self):
        return 'title: ' + self.title + ' ' + 'filename: ' + str(self.filename)

    