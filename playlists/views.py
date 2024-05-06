from django.shortcuts import render, redirect
from playlists.models import *
from django.http import HttpRequest, HttpResponse


# Create your views here.
def display_all_playlists(request: HttpRequest) -> HttpResponse:
    """
    View function to display user's playlists.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered response with user's playlists.
    """
    playlists = Playlist.objects.filter(user=request.user)
    count = playlists.count()
    if count == 0:
        playlists = None
    return render(request, 'playlists/playlists.html', {'playlists': playlists})


def create_playlist(request: HttpRequest) -> HttpResponse:
    """
    View function to create a new playlist.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered response with form to create a playlist.
    """
    if request.method == 'GET':
        songs = Song.objects.filter(user=request.user)
        count = songs.count()
        if count == 0:
            songs = None
        return render(request, 'playlists/createPlaylist.html', {'songs': songs})
    elif request.method == 'POST':
        playlist_name = request.POST.get('play_name')
        songs = request.POST.getlist('songs[]')
        no_of_songs = len(songs)
        playlist = Playlist(user=request.user, playlist_name=playlist_name, number_of_songs=no_of_songs)
        playlist.save()
        for i in range(no_of_songs):
            song = Song.objects.get(id=songs[i])
            play_song = Playlist_songs(playlist=playlist, song=song)
            play_song.save()
        return redirect('displayPlaylist', playlist.id)


def display_playlist(request: HttpRequest, playlist_id: int) -> HttpResponse:
    """
    View function to display a playlist.

    Args:
        request (HttpRequest): The HTTP request object.
        playlist_id (int): The ID of the playlist to display.

    Returns:
        HttpResponse: Rendered response with the playlist.
    """
    playlist = Playlist.objects.get(id=playlist_id)
    playlist_songs = Playlist_songs.objects.filter(playlist=playlist)
    return render(request, 'playlists/displayPlaylist.html',
                  {'plays': playlist_songs, 'playlist': playlist})


def delete_playlist(request: HttpRequest, playlist_id: int) -> HttpResponse:
    """
    View function to delete a playlist.

    Args:
        request (HttpRequest): The HTTP request object.
        playlist_id (int): The ID of the playlist to delete.

    Returns:
        HttpResponse: Redirects to the user's playlists page.
    """
    playlist = Playlist.objects.get(id=playlist_id)
    playlist.delete()
    return redirect('users-playlists')


def remove_song(request: HttpRequest, song_id: int) -> HttpResponse:
    """
    View function to remove a song from a playlist.
    Args:
        request (HttpRequest): The HTTP request object.
        song_id (int): The ID of the song to remove.
    Returns:
        HttpResponse: Redirects to the playlist display page.
    """
    play_song = Playlist_songs.objects.get(id=song_id)
    playlist = play_song.playlist
    play_song.delete()
    playlist.number_of_songs -= 1
    playlist.save()
    return redirect('displayPlaylist', play_song.playlist.id)


def play_entire_playlist(request: HttpRequest, playlist_id: int) -> HttpResponse:
    """
    View function to play the entire playlist.

    Args:
        request (HttpRequest): The HTTP request object.
        playlist_id (int): The ID of the playlist to play.

    Returns:
        HttpResponse: Rendered response with the playlist songs.
    """

    playlist = Playlist.objects.get(id=playlist_id)
    playlist_song = Playlist_songs.objects.filter(playlist=playlist).first()
    song = playlist_song.song.song_name
    play_songs = Playlist_songs.objects.filter(playlist=playlist)
    songs = []
    for i in play_songs:
        songs.append(i.song)  
    count = len(songs)
    if count == 0:
        songs = None
    return render(request, 'songs/player.html', {'songs': songs, 'curr_song': song})
    

def play_song_of_playlist(request: HttpRequest, song_id: int) -> HttpResponse:
    """
    View function to play a specific song from a playlist.

    Args:
        request (HttpRequest): The HTTP request object.
        song_id (int): The ID of the song to play.

    Returns:
        HttpResponse: Rendered response with the playlist songs.
    """
    play = Playlist_songs.objects.get(id=song_id)
    song = play.song.song_name
    playlist = play.playlist
    play_songs = Playlist_songs.objects.filter(playlist=playlist)
    songs = []
    for i in play_songs:
        songs.append(i.song)  
    count = len(songs)
    if count == 0:
        songs = None
    return render(request, 'songs/player.html', {'songs': songs, 'curr_song': song})


def add_song(request: HttpRequest) -> HttpResponse:
    """
    View function to add a song to a playlist.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the user's playlists page.
    """
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist')
        playlist = Playlist.objects.get(id=playlist_id)
        song_id = request.POST.get('song')
        song = Song.objects.get(id=song_id)
        play_song = Playlist_songs(playlist=playlist, song=song)
        play_song.save()
        playlist.number_of_songs += 1
        playlist.save()
        return redirect('users-playlists')


def get_number_of_songs(request: HttpRequest, playlist_id: int) -> int:
    """
    Retrieves the number of songs in a playlist.

    Args:
        request (HttpRequest): The HTTP request object.
        playlist_id (int): The ID of the playlist.

    Returns:
        int: The number of songs in the playlist.
    """
    playlist = Playlist.objects.get(id=playlist_id)
    no = playlist.number_of_songs
    return no






    
