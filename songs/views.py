from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from playlists.models import *
from django.http import HttpRequest, HttpResponse
from typing import Union


def get_users_songs(request: HttpRequest) -> HttpResponse:
    """
    View function to display user's songs and playlists.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered response with user's songs and playlists.
    """
    songs = Song.objects.filter(user=request.user)
    count = songs.count()
    if count == 0:
        songs = None
    playlists = Playlist.objects.filter(user=request.user)
    count = playlists.count()
    if count == 0:
        playlists = None
    return render(request, 'songs/songs.html', {'songs': songs, 'playlists': playlists})


def play_song(request: HttpRequest, song_id: int) -> HttpResponse:
    """
    View function to play a specific song.

    Args:
        request (HttpRequest): The HTTP request object.
        song_id (int): The ID of the song to play.

    Returns:
        HttpResponse: Rendered response with the player and the song to play.
    """
    song = Song.objects.get(id=song_id)
    song = song.song_name
    songs = Song.objects.filter(user=request.user)
    count = songs.count()
    if count == 0:
        songs = None
    return render(request, 'songs/player.html', {'songs': songs, 'curr_song': song})


def add_song(request: HttpRequest) -> Union[HttpResponse, redirect]:
    """
    View function to add a new song.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Union[HttpResponse, redirect]: Redirects to the user's songs page after adding the song.
    """
    if request.method == "POST":
        song = request.FILES['song']
        store = FileSystemStorage()
        song_name = song.name
        name = store.save(song.name, song)
        url = store.url(name)
        emotion = request.POST["emotion"]
        song = Song(user=request.user, song_name=song_name, song_url=url, emotion=emotion)
        song.save()
        return redirect('users-songs')


def remove_song(request: HttpRequest, song_id: int) -> HttpResponse:
    """
    View function to remove a song.

    Args:
        request (HttpRequest): The HTTP request object.
        song_id (int): The ID of the song to remove.

    Returns:
        HttpResponse: Redirects to the user's songs page after removing the song.
    """
    song = Song.objects.get(id=song_id)
    song.delete()
    return redirect('users-songs')


def get_song_name(request: HttpRequest, song_id: int) -> str:
    """
    Retrieves the name of a song.

    Args:
        request (HttpRequest): The HTTP request object.
        song_id (int): The ID of the song.

    Returns:
        str: The name of the song.
    """
    song = Song.objects.get(id=song_id)
    return song.song_name


def get_url(request: HttpRequest, song_id: int) -> str:
    """
    Retrieves the URL of a song.

    Args:
        request (HttpRequest): The HTTP request object.
        song_id (int): The ID of the song.

    Returns:
        str: The URL of the song.
    """
    song = Song.objects.get(id=song_id)
    return song.song_url
