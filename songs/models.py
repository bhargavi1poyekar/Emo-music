from django.db import models
from django.contrib.auth.models import User


class Song(models.Model):
	"""
	Model representing a song uploaded by a user.

	Each song is associated with a user through a ForeignKey relationship.

	Attributes:
		user (ForeignKey): The user who uploaded the song.
		song_name (CharField): The name of the song.
		song_url (CharField): The URL of the song file.
		mood_options (list of tuples): Choices for the mood/emotion of the song.
		emotion (CharField): The mood/emotion of the song.
	"""

	user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
	song_name = models.CharField(max_length=100)
	song_url = models.CharField(max_length=400)
	mood_options = [('sad', 'sad'), ('happy', 'happy'), ('normal', 'normal')]
	emotion = models.CharField(max_length=50, choices=mood_options, default='normal')
	
	def __str__(self):
		return f'{self.song_name} with {self.emotion}'

