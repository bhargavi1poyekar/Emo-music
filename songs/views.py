from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from typing import Union
from typing import Optional, List
from playlists.models import Song, Playlist


def return_none_if_empty(object):
    """
    Check if the provided object (list or queryset) is empty and return None if so.

    Args:
        object (List): A list or queryset to be checked.

    Returns:
        Optional[List]: The original object or None if it's empty.
    """
    count = len(object) if isinstance(object, list) else object.count()
    return None if count == 0 else object


def get_playlists_of_user(user):
    """
    Retrieves all playlists associated with a specific user.

    Args:
       user (User): The user whose playlists are to be retrieved.

    Returns:
       Optional[List[Playlist]]: A list of Playlist objects if any are found, or None if the user has no playlists.
    """
    playlists = Playlist.objects.filter(user=user)
    return return_none_if_empty(playlists)


def get_songs_of_user(user):
    """
    Retrieves all songs associated with a specific user.

    Args:
        user (User): The user whose songs are to be retrieved.

    Returns:
        Optional[List[Song]]: A list of Song objects if any are found, or None if the user has no songs.
    """
    songs = Song.objects.filter(user=user)
    return return_none_if_empty(songs)


def get_song_name(song):
    """
    Retrieves the name of a given song.

    Args:
        song (Song): The Song object from which to retrieve the name.

    Returns:
        str: The name of the song.
    """
    return song.song_name


def get_song_from_id(song_id):
    """
    Retrieves a song by its ID.

    Args:
        song_id (int): The unique identifier of the song.

    Returns:
        Song: The Song object corresponding to the given ID.
    """
    return Song.objects.get(id=song_id)


def get_users_songs(request: HttpRequest) -> HttpResponse:
    """
    View function to display user's songs and playlists.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered response with user's songs and playlists.
    """
    songs = get_songs_of_user(request.user)
    playlists = get_playlists_of_user(request.user)
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
    song = get_song_name_from_id(song_id)
    songs = get_songs_of_user(request.user)
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
    song = get_song_from_id(song_id)
    song.delete()
    return redirect('users-songs')


def get_song_name_from_id(song_id: int) -> str:
    """
    Retrieves the name of a song.

    Args:
        song_id (int): The ID of the song.

    Returns:
        str: The name of the song.
    """
    song = get_song_from_id(song_id)
    return get_song_name(song)


def get_url(request: HttpRequest, song_id: int) -> str:
    """
    Retrieves the URL of a song.

    Args:
        request (HttpRequest): The HTTP request object.
        song_id (int): The ID of the song.

    Returns:
        str: The URL of the song.
    """
    song = get_song_from_id(song_id)
    return song.song_url
