from django.contrib import admin

# Register your models here.
from .models import (
    Playlist,
    Track
)

admin.site.register(Playlist)
admin.site.register(Track)