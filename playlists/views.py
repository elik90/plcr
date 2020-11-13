from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

#from .forms import PlaylistModelForm
from .forms import (
    PlaylistModelForm,
    UploadFileForm,
    PlaylistForm,
    GenerateTracklistForm
)
from .models import Playlist

def search_view(request, *args, **kwargs):
    query = request.GET.get('q')
    qs = Playlist.objects.filter(title__icontains=query[0])
    print(query,qs)
    context = {"name":"Justin", "query": query}
    return render(request, "home.html", context)

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

#########################################################################
def home_view(request):
    all_playlists = Playlist.objects.all()
    return render(request, 'home.html', {'playlists':all_playlists})


# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form':form})

# def handle_uploaded_file(f):
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document'] # document matches html input
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

def playlist_list(request):
    playlists = Playlist.objects.all().order_by('id')
    return render(request, 'playlist_list.html', {
        'playlists': playlists
    })

def gtpl(request):
    if request.method == 'POST':
        print("in gtpl")
        playlist_id = request.POST.get('playlist_id')
        print(playlist_id)
        playlist_obj = Playlist.objects.get(id=playlist_id)
        print(playlist_obj)
        if playlist_obj.isgenerated == False:
            playlist_obj.isgenerated = True
        else:
            playlist_obj.isgenerated = False
        playlist_obj.save()
        return redirect('playlist_list')
    # else:
    #     return redirect('')




def upload_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('playlist_list')
    else:
        form = PlaylistForm()
    return render(request, 'upload_playlist.html', {
        'form': form
    })
