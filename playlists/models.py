from django.db import models
from django.contrib.auth.models import User
from songs.models import Song

# Create your models here.
class Playlist(models.Model):
	user = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
	playlist_name=models.CharField(max_length=100)
	number_of_songs=models.IntegerField()

	def __str__(self):
		return f'{self.playlist_name}'

class Playlist_songs(models.Model):
	playlist=models.ForeignKey(Playlist,default=None,on_delete=models.CASCADE)
	song=models.ForeignKey(Song,default=None,on_delete=models.CASCADE)
