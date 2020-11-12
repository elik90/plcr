"""bootcamp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from playlists import views... not advantageous if importing views from other apps
from playlists.views import (
    playlist_create_view,
    search_view,
    playlist_detail_view,
    playlist_list_view,
    home_view,
    upload,
    playlist_list,
    upload_playlist
)


urlpatterns = [

    path('search/', search_view),
    path('playlists/', playlist_list_view),
    path('playlists/create/', playlist_create_view),
    path('playlists/<int:pk>/', playlist_detail_view),
    # path('playlists/1/', views.playlist_detail_view),
    path('admin/', admin.site.urls),
    path('', home_view),
    path('upload/', upload, name='upload'),
    path('playlist/list/', playlist_list, name='playlist_list'),
    path('playlist/upload/', upload_playlist, name='upload_playlist')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

