from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect

from .forms import PlaylistModelForm
from .models import Playlist
# Create your views here.
def search_view(request, *args, **kwargs):
    query = request.GET.get('q')
    qs = Playlist.objects.filter(title__icontains=query[0])
    print(query,qs)
    context = {"name":"Justin", "query": query}
    return render(request, "home.html", context)

# def playlist_create_view(request, *args, **kwargs):
#     # print(request.POST)
#     # print(request.GET)
#     if request.method == "POST":
#         post_data = request.POST or None
#         if post_data != None:
#             my_form = PlaylistForm(request.POST)
#             if my_form.is_valid():
#                 print(my_form.cleaned_data.get("title"))
#                 title_from_input = my_form.cleaned_data.get("title")
#                 Playlist.objects.create(title=title_from_input)
#                 #print("post_data", post_data)
#     return render(request, "forms.html", {})

def playlist_create_view(request, *args, **kwargs):
    form = PlaylistModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # do some stuff
        # ojb.user = request.user
        obj.save()

        # print(form.cleaned_data)
        # data = form.cleaned_data
        # Playlist.objects.create(**data)
        form = PlaylistModelForm() # reinitialize form
        # return HttpResponseRedirect("/success")
        # return redirect("/success")
    return render(request, "forms.html", {"form": form})

def playlist_detail_view(request, pk, *args, **kwargs):
    try:
        obj = Playlist.objects.get(pk=pk)
    except Playlist.DoesNotExist: 
        raise Http404   
    return render(request, "playlists/detail.html", {"object":obj})

def playlist_list_view(request, *args, **kwargs):
    qs = Playlist.objects.all()
    context = {"object_list": qs}
    return render(request, "playlists/list.html", context)

# class HomeView():
#     pass