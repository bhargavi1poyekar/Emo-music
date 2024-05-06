from django.db import models
from django.contrib.auth.models import User
from songs.models import Song


# Create your models here.
class Playlist(models.Model):
	"""
	Model representing a playlist created by a user.

	Each playlist is associated with a user through a ForeignKey relationship.

	Attributes:
		user (ForeignKey): The user who created the playlist.
		playlist_name (CharField): The name of the playlist.
		number_of_songs (IntegerField): The number of songs in the playlist.
	"""
	user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
	playlist_name = models.CharField(max_length=100)
	number_of_songs = models.IntegerField()

	def __str__(self):
		return f'{self.playlist_name}'


class Playlist_songs(models.Model):
	"""
	Model representing the songs in a playlist.

	Each playlist song entry is associated with a playlist and a song through ForeignKey relationships.

	Attributes:
		playlist (ForeignKey): The playlist to which the song belongs.
		song (ForeignKey): The song included in the playlist.
	"""
	playlist = models.ForeignKey(Playlist, default=None, on_delete=models.CASCADE)
	song = models.ForeignKey(Song, default=None, on_delete=models.CASCADE)
