from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from users.models import *
from songs.models import *
from playlists.models import *
from django.contrib.auth.models import User

# Create your views here.
def playlists(request):
    playlists=Playlist.objects.filter(user=request.user)
    count=playlists.count()
    if count==0:
        playlists=None 
    
    return render(request,'playlists/playlists.html',{'playlists':playlists})

def createPlaylist(request):
    if request.method == 'GET':
        songs=Song.objects.filter(user=request.user)
        count=songs.count()
        if count==0:
            songs=None 
        return render(request,'playlists/createPlaylist.html',{'songs':songs})
    elif request.method == 'POST':
        playlist_name=request.POST.get('play_name')
        songs=request.POST.getlist('songs[]')
        no_of_songs=len(songs)
        playlist=Playlist(user=request.user,playlist_name=playlist_name,number_of_songs=no_of_songs)
        playlist.save()
        for i in range(no_of_songs):
            song=Song.objects.get(id=songs[i])
            play_song=Playlist_songs(playlist=playlist,song=song)
            play_song.save()
        return redirect('displayPlaylist',playlist.id)

def displayPlaylist(request,id):
    playlist=Playlist.objects.get(id=id)
    plays=Playlist_songs.objects.filter(playlist=playlist)
    return render(request,'playlists/displayPlaylist.html',{'plays':plays,'playlist':playlist})

def deletePlaylist(request,id):
    play=Playlist.objects.get(id=id)
    play.delete()
    return redirect('users-playlists')

def removeSong(request,id):
    play_song=Playlist_songs.objects.get(id=id)
    playlist=play_song.playlist
    play_song.delete()
    playlist.number_of_songs-=1
    playlist.save()
    return redirect('displayPlaylist',play_song.playlist.id)

def playEntirePlaylist(request,id):
    playlist=Playlist.objects.get(id=id)
    play=Playlist_songs.objects.filter(playlist=playlist).first()
    song=play.song.song_name
    play_songs=Playlist_songs.objects.filter(playlist=playlist)
    songs=[]
    for i in play_songs:
        songs.append(i.song)  
    count=len(songs)
    if count==0:
        songs=None
    return render(request,'songs/player.html', {'songs':songs,'curr_song':song})
    

def playSongofPlaylist(request,id):
    play=Playlist_songs.objects.get(id=id)
    song=play.song.song_name
    playlist=play.playlist
    print(playlist)
    play_songs=Playlist_songs.objects.filter(playlist=playlist)
    songs=[]
    for i in play_songs:
        songs.append(i.song)  
    count=len(songs)
    if count==0:
        songs=None
    return render(request,'songs/player.html', {'songs':songs,'curr_song':song})

def addSong(request):
    if request.method=='POST':
        playlist_id=request.POST.get('playlist')
        playlist=Playlist.objects.get(id=playlist_id)
        song_id=request.POST.get('song')
        song=Song.objects.get(id=song_id)
        play_song=Playlist_songs(playlist=playlist,song=song)
        play_song.save()
        playlist.number_of_songs+=1
        playlist.save()
        return redirect('users-playlists')

def getNumberOfSongs(request,id):
    playlist=Playlist.objects.get(id=id)
    no=playlist.number_of_songs
    return no






    
