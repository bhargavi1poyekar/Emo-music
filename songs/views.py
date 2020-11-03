from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from users.models import *
from songs.models import *
from playlists.models import *
from django.contrib.auth.models import User

def songs(request):
    songs=Song.objects.filter(user=request.user)
    count=songs.count()
    if count==0:
        songs=None 
    playlists=Playlist.objects.filter(user=request.user)
    count=playlists.count()
    if count==0:
        playlists=None
    return render(request,'songs/songs.html',{'songs':songs,'playlists':playlists})

def playSong(request,id):
    song=Song.objects.get(id=id)
    song=song.song_name
    songs=Song.objects.filter(user=request.user)
    count=songs.count()
    if count==0:
        songs=None
    return render(request,'songs/player.html', {'songs':songs,'curr_song':song})

def addSong(request):
    if request.method=="POST":
        song=request.FILES['song']
        store=FileSystemStorage()
        song_name=song.name
        name=store.save(song.name,song)
        url=store.url(name)
        emotion=request.POST["emotion"]
        song=Song(user=request.user,song_name=song_name,song_url=url,emotion=emotion)
        song.save()
        return redirect('users-songs')

def removeSong(request,id):
    song=Song.objects.get(id=id)
    song.delete()
    return redirect('users-songs')

def getSongName(request,id):
    song=Song.objects.get(id=id)
    return song.song_name

def getUrl(request,id):
    song=Song.objects.get(id=id)
    return song.song_url
