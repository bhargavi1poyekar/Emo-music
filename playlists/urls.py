from django.urls import path,include
from . import views as play_view


urlpatterns = [
   	path('',play_view.playlists,name='users-playlists'),
	path('display/<int:id>',play_view.displayPlaylist,name='displayPlaylist'),
	path('addSong/',play_view.addSong,name='add-song-playlist'),
	path('removeSong/<int:id>',play_view.removeSong,name='removeSong'),
    path('create/',play_view.createPlaylist,name='create-playlist'),
    path('delete/<int:id>',play_view.deletePlaylist,name='del-playlist'),
    path('playSong/<int:id>',play_view.playSongofPlaylist,name='play-song-playlist'),
    path('playPlaylist/<int:id>',play_view.playEntirePlaylist,name='play-playlist'),
]