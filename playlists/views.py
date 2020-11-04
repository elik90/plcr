from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Playlist
# Create your views here.
def home_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Hello world</h1>")
    context = {"name":"Justin"}
    return render(request, "home.html", context)

def playlist_detail_view(request, pk, *args, **kwargs):
    try:
        obj = Playlist.objects.get(pk=pk)
    except Playlist.DoesNotExist: 
        raise Http404   
    # return HttpResponse(f"Playlist id {obj.pk}")


    return render(request, "playlists/detail.html", {"object":obj})

def playlist_list_view(request, *args, **kwargs):
    qs = Playlist.objects.all()
    context = {"object_list": qs}
    return render(request, "playlists/list.html", context)
# class HomeView():
#     pass