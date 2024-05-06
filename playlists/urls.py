from django.urls import path
from . import views as play_view


urlpatterns = [
    path('', play_view.display_all_playlists, name='users-playlists'),
    path('display/<int:playlist_id>', play_view.display_playlist, name='displayPlaylist'),
    path('addSong/', play_view.add_song, name='add-song-playlist'),
    path('removeSong/<int:song_id>', play_view.remove_song, name='removeSong'),
    path('create/', play_view.create_playlist, name='create-playlist'),
    path('delete/<int:playlist_id>', play_view.delete_playlist, name='del-playlist'),
    path('playSong/<int:song_id>', play_view.play_song_of_playlist, name='play-song-playlist'),
    path('playPlaylist/<int:playlist_id>', play_view.play_entire_playlist, name='play-playlist'),
]
