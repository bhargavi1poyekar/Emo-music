from django.urls import path
from . import views as songs_view


urlpatterns = [
	path('', songs_view.get_users_songs, name='users-songs'),
	path('play/<int:song_id>', songs_view.play_song, name='play-songs'),
	path('add/', songs_view.add_song, name='add-song'),
	path('delete/<int:song_id>', songs_view.remove_song, name='del-song'),
]
