from django.db import models



class Playlist(models.Model):
	name=models.CharField(max_length=100)
	number_of_songs=models.IntegerField()

	def __str__(self):
		return f'{self.name} with  {self.mood}'




class Song(models.Model):
	name= models.CharField(max_length=100)
	storage_name=models.CharField(max_length=100)
	mood_options=[('sad', 'sad'),('happy', 'happy'),('normal','normal')]
	mood = models.CharField(max_length=50,choices=mood_options,default='normal')
	playlist = models.ForeignKey(Playlist,on_delete=models.PROTECT)
	def __str__(self):
		return f'{self.name} with {self.mood}  '









