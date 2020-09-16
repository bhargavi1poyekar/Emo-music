from django.db import models
from django.contrib.auth.models import User

class Playlist(models.Model):
	user = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
	playlist_name=models.CharField(max_length=100)
	number_of_songs=models.IntegerField()

	def __str__(self):
		return f'{self.playlist_name}'

class Song(models.Model):
	user = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
	song_name= models.CharField(max_length=100)
	song_url=models.CharField(max_length=100)
	mood_options=[('sad', 'sad'),('happy', 'happy'),('normal','normal')]
	emotion = models.CharField(max_length=50,choices=mood_options,default='normal')
	
	def __str__(self):
		return f'{self.song_name} with {self.emotion}'









