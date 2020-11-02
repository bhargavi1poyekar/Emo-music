
from django.urls import path,include
from . import views as songs_view


urlpatterns = [
   	path('',songs_view.songs,name='users-songs'),
	path('play/<int:id>',songs_view.playSong,name='play-songs'),
	path('add/',songs_view.addSong,name='add-song'),
	path('delete/<int:id>',songs_view.removeSong,name='del-song'),
]