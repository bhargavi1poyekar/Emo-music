from django.shortcuts import render, redirect
from playlists.models import Playlist, Song, Playlist_songs
from django.http import HttpRequest, HttpResponse
from typing import Optional, List
from songs.views import get_songs_of_user, get_song_from_id, return_none_if_empty, get_playlists_of_user


# Create your views here.

def display_all_playlists(request: HttpRequest) -> HttpResponse:
    """
    View function to display user's playlists.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered response with user's playlists.
    """
    playlists = get_playlists_of_user(request.user)
    return render(request, 'playlists/playlists.html', {'playlists': playlists})


def add_song_to_playlist(song_id: int, playlist: Playlist) -> None:
    """
    Adds a song to a playlist based on the song ID.

    Args:
        song_id (int): The unique identifier for the song.
        playlist (Playlist): The playlist object to which the song will be added.
    """
    song = get_song_from_id(song_id)
    play_song = Playlist_songs(playlist=playlist, song=song)
    play_song.save()


def get_playlist_from_id(playlist_id: int) -> Playlist:
    """
    Retrieves a playlist by its ID.

    Args:
        playlist_id (int): The unique identifier for the playlist.

    Returns:
        Playlist: The playlist object corresponding to the given ID.
    """
    return Playlist.objects.get(id=playlist_id)


def get_songs_from_playlist(playlist: Playlist) -> List[Playlist_songs]:
    """
    Retrieves all songs from a specific playlist.

    Args:
        playlist (Playlist): The playlist object from which songs are retrieved.

    Returns:
        List[Playlist_songs]: A list of Playlist_songs objects associated with the playlist.
    """
    return Playlist_songs.objects.filter(playlist=playlist)


def get_song_from_playlist(song_id: int) -> Playlist_songs:
    """
    Retrieves a specific song in a playlist by its ID.

    Args:
        song_id (int): The unique identifier for the playlist song.

    Returns:
        Playlist_songs: The Playlist_songs object corresponding to the given song ID.
    """
    return Playlist_songs.objects.get(id=song_id)


def create_playlist(request: HttpRequest) -> HttpResponse:
    """
    View function to create a new playlist.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered response with form to create a playlist.
    """
    if request.method == 'GET':
        songs = get_songs_of_user(request.user)
        songs = return_none_if_empty(songs)
        return render(request, 'playlists/createPlaylist.html', {'songs': songs})
    elif request.method == 'POST':
        playlist_name = request.POST.get('play_name')
        songs = request.POST.getlist('songs[]')
        no_of_songs = len(songs)
        playlist = Playlist(user=request.user, playlist_name=playlist_name, number_of_songs=no_of_songs)
        playlist.save()
        for i in range(no_of_songs):
            add_song_to_playlist(songs[i], playlist)
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
    playlist = get_playlist_from_id(playlist_id)
    playlist_songs = get_songs_from_playlist(playlist)
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
    playlist = get_playlist_from_id(playlist_id)
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
    play_song = get_song_from_playlist(song_id)
    playlist = play_song.playlist
    play_song.delete()
    playlist.number_of_songs -= 1
    playlist.save()
    return redirect('displayPlaylist', play_song.playlist.id)


def get_songs_to_play(play_songs: List[Playlist_songs]):
    """
    Retrieves a list of Song objects from a list of Playlist_songs objects.

    Args:
        play_songs (List[Playlist_songs]): A list of Playlist_songs objects.

    Returns:
        Optional[List[Song]]: A list of Song objects, or None if no songs are available.
    """

    songs = []
    for i in play_songs:
        songs.append(i.song)
    songs = return_none_if_empty(songs)
    return songs


def get_song_name(playlist_song: Playlist_songs) -> str:
    """
    Retrieves the name of a song from a Playlist_songs object.

    Args:
        playlist_song (Playlist_songs): The Playlist_songs object.

    Returns:
        str: The name of the song.
    """
    return playlist_song.song.song_name


def play_entire_playlist(request: HttpRequest, playlist_id: int) -> HttpResponse:
    """
    View function to play the entire playlist.

    Args:
        request (HttpRequest): The HTTP request object.
        playlist_id (int): The ID of the playlist to play.

    Returns:
        HttpResponse: Rendered response with the playlist songs.
    """

    playlist = get_playlist_from_id(playlist_id)
    play_songs = get_songs_from_playlist(playlist)
    playlist_song = play_songs.first()
    song = get_song_name(playlist_song)
    songs = get_songs_to_play(play_songs)

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
    play = get_song_from_playlist(song_id)
    song = get_song_name(play)
    playlist = play.playlist
    play_songs = get_songs_from_playlist(playlist)
    songs = get_songs_to_play(play_songs)

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
        playlist = get_playlist_from_id(playlist_id)
        song_id = request.POST.get('song')
        add_song_to_playlist(song_id, playlist)
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
    playlist = get_playlist_from_id(playlist_id)
    num_songs = playlist.number_of_songs
    return num_songs






    
