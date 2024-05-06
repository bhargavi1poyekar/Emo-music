from django.shortcuts import redirect
from . import emotion_model
from Image.models import Image
from playlists.models import Playlist, Playlist_songs
from songs.models import Song
from django.contrib.auth.models import User
from pathlib import Path
import random
from django.db.models import QuerySet
from typing import Union
from django.http import HttpRequest

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# Create your views here.


def get_model_paths() -> tuple:
    """
    Get the paths for the emotion recognition model JSON and weights files.

    Returns:
        tuple: Paths for model JSON file and model weights file.
    """
    model_json_path = str(BASE_DIR) + "/emotion/model_config.json"
    model_weights_path = str(BASE_DIR) + "/emotion/model_wts.h5"
    return model_json_path, model_weights_path


def get_image_path(request) -> str:
    """
    Get the path to the user's image file.

    Args:
        request: The HTTP request object.

    Returns:
        str: Path to the user's image file.
    """
    image = Image.objects.get(user=request.user)
    image_url = image.Image_url
    return str(BASE_DIR) + "/media/" + str(image_url)


def get_or_create_playlist(user: User, playlist_name: str) -> Playlist:
    """
    Get or create a playlist with the given name for the specified user.

    Args:
        user (User): The user for whom the playlist is being created.
        playlist_name (str): The name of the playlist.

    Returns:
        Playlist: The playlist object.
    """
    admin = User.objects.get(username='admin')
    playlist = Playlist.objects.filter(user=admin, playlist_name=playlist_name).first()
    if playlist:
        playlist.delete()
    playlist = Playlist(user=admin, playlist_name=playlist_name, number_of_songs=-1)
    playlist.save()
    return playlist


def add_songs_to_playlist(playlist: Playlist, songs: QuerySet) -> None:
    """
    Add songs to the specified playlist.

    Args:
        playlist (Playlist): The playlist to which songs are being added.
        songs (QuerySet): The queryset of songs to add to the playlist.
    """
    for song in songs:
        relation = Playlist_songs(playlist=playlist, song=song)
        relation.save()


def create_playlist(request, emotion: str) -> int:
    """
    Create a playlist based on the predicted emotion.

    Args:
        request: The HTTP request object.
        emotion (str): The predicted emotion.

    Returns:
        int: The ID of the created playlist.
    """
    playlist_name = f"{request.user.username}_{emotion}"
    playlist = get_or_create_playlist(request.user, playlist_name)
    user_songs = Song.objects.filter(user=request.user, emotion=emotion)
    admin_songs = Song.objects.filter(user__username='admin', emotion=emotion)
    add_songs_to_playlist(playlist, user_songs)
    add_random_songs_to_playlist(playlist, admin_songs)
    return playlist.id


def add_random_songs_to_playlist(playlist: Playlist, admin_songs: QuerySet) -> None:
    """
    Add random songs from admin's songs to the specified playlist.

    Args:
        playlist (Playlist): The playlist to which random songs are being added.
        admin_songs (QuerySet): The queryset of admin's songs to select random songs from.
    """
    song_count = admin_songs.count()
    sampling = set(random.sample(list(range(0, song_count)), k=min(10, song_count)))
    order = [*range(song_count)]
    random.shuffle(order)
    for i in range(song_count):
        if order[i] in sampling:
            relation = Playlist_songs(playlist=playlist, song=admin_songs[order[i]])
            relation.save()


def detect_emotion(request: HttpRequest):
    """
    Detects emotion from the user's image and processes the result.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Tuple[str, Any]: A tuple containing the redirect destination and any additional arguments.
    """
    model_json_path, model_weights_path = get_model_paths()
    img_path = get_image_path(request)
    face_expression = emotion_model.FacialExpressionModel(model_json_path, model_weights_path, img_path)
    image = Image.objects.get(user=request.user)
    image.delete()
    return_val, processed_img = face_expression.preprocess_img()
    return process_return_val(request, return_val, processed_img, face_expression)


def process_return_val(request, return_val, processed_img, face_expression):
    """
    Processes the return value from emotion detection.
    Args:
        request (HttpRequest): The HTTP request object.
        return_val (str): The return value indicating the result of emotion detection.
        processed_img (Any): The processed image data.
        face_expression (FacialExpressionModel): The facial expression model instance.
    Returns:
        Tuple[str, Any]: A tuple containing the redirect destination and any additional arguments.
    """
    to, args = 'error-page', "Some error"
    if return_val == "noFace":
        to, args = "error-page", "No Face detected for given image, try again with a new image."
    elif return_val == "mulFace":
        to, args = "error-page", "Multiple Faces detected for given image, try again with a new image."
    elif return_val == "exception":
        to, args = "error-page", "An Unknown Error Occurred, Please Try Again."

    emotion = ""
    if return_val:
        success = face_expression.predict_emotion(processed_img)
        if success:
            emotion = face_expression.get_emotions()
            print(f'Emotion: {emotion}')
            playlist_id = create_playlist(request, emotion)
            to, args = 'displayPlaylist', playlist_id

    return to, args


def get_playlist_from_emotion(request) -> Union[redirect]:
    """
    Predict emotion from the user's image and create a playlist accordingly.

    Args:
        request: The HTTP request object.

    Returns:
        Union[redirect]: Redirects to the error page if an error occurs, otherwise redirects to the display playlist page.
    """
    to, args = detect_emotion(request)
    return redirect(to, args)
