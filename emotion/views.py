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
    try:
        # Assume BASE_DIR is defined elsewhere in the global scope or environment
        model_json_path = str(BASE_DIR) + "/emotion/model_config.json"
        model_weights_path = str(BASE_DIR) + "/emotion/model_wts.h5"

        # Basic check to see if paths are created properly (this doesn't check if paths exist)
        if not model_json_path or not model_weights_path:
            raise ValueError("Model paths could not be constructed. Check BASE_DIR setting.")

        return model_json_path, model_weights_path

    except NameError as e:
        # This will catch if BASE_DIR is not defined
        raise ValueError(f"Configuration error: {e}")

    except Exception as e:
        # General catch-all for any other unexpected exceptions
        raise ValueError(f"An unexpected error occurred when getting model paths: {e}")


def get_image_path(request) -> str:
    """
    Get the path to the user's image file.

    Args:
        request: The HTTP request object.

    Returns:
        str: Path to the user's image file.
    """
    try:
        # Attempt to retrieve the user's image from the database
        image = Image.objects.get(user=request.user)
        image_url = image.Image_url

        # Construct the full file path
        full_path = str(BASE_DIR) + "/media/" + str(image_url)

        # Check if the path string is correctly constructed
        if not full_path:
            raise ValueError("Failed to construct the image file path.")
        return full_path

    except AttributeError as e:
        raise ValueError(f"Attribute error: Missing necessary properties in the"
                         f"request or image object. {e}")

    except Exception as e:
        # General catch-all for any other unexpected exceptions
        raise ValueError(f"An unexpected error occurred while retrieving the image path: {e}")


def get_or_create_playlist(user: User, playlist_name: str) -> Playlist:
    """
    Get or create a playlist with the given name for the specified user.

    Args:
        user (User): The user for whom the playlist is being created.
        playlist_name (str): The name of the playlist.

    Returns:
        Playlist: The playlist object.
    """
    try:
        # Check for any empty or invalid input arguments
        if not user or not playlist_name:
            raise ValueError("Invalid user or playlist name provided.")

        admin = User.objects.get(username='admin')
        playlist = Playlist.objects.filter(user=admin, playlist_name=playlist_name).first()
        if playlist:
            playlist.delete()
        playlist = Playlist(user=admin, playlist_name=playlist_name, number_of_songs=-1)
        playlist.save()
        return playlist

    except Exception as e:
        # General catch-all for any other unexpected exceptions
        raise ValueError(f"An unexpected error occurred: {e}")


def add_songs_to_playlist(playlist: Playlist, songs: QuerySet) -> None:
    """
    Add songs to the specified playlist.

    Args:
        playlist (Playlist): The playlist to which songs are being added.
        songs (QuerySet): The queryset of songs to add to the playlist.
    """
    try:

        for song in songs:
            relation = Playlist_songs(playlist=playlist, song=song)
            relation.save()

    except AttributeError as e:
        # Handle attribute errors in case of incorrect model definitions or method calls
        raise ValueError(f"An attribute error occurred: {e}")

    except Exception as e:
        # General catch-all for any other unexpected exceptions
        raise ValueError(f"An unexpected error occurred while adding songs to the playlist: {e}")


def create_playlist(request, emotion: str) -> int:
    """
    Create a playlist based on the predicted emotion.

    Args:
        request: The HTTP request object.
        emotion (str): The predicted emotion.

    Returns:
        int: The ID of the created playlist.
    """
    try:
       
        # Generate a unique playlist name based on the user's username and the emotion
        playlist_name = f"{request.user.username}_{emotion}"

        # Get or create a new playlist
        playlist = get_or_create_playlist(request.user, playlist_name)

        # Fetch songs based on the user and emotion
        user_songs = Song.objects.filter(user=request.user, emotion=emotion)
        admin_songs = Song.objects.filter(user__username='admin', emotion=emotion)

        # Add songs to the playlist
        add_songs_to_playlist(playlist, user_songs)
        add_songs_to_playlist(playlist, admin_songs)  # Assuming add_random_songs_to_playlist does a similar job
        return playlist.id
    except AttributeError as e:
        # Catch errors related to attribute accesses (e.g., request.user)
        raise ValueError(f"An error occurred due to missing or invalid attribute: {e}")
    except Exception as e:
        # General catch-all for any other exceptions
        raise ValueError(f"An unexpected error occurred while creating the playlist: {e}")


def add_random_songs_to_playlist(playlist: Playlist, admin_songs: QuerySet) -> None:
    """
    Add random songs from admin's songs to the specified playlist.

    Args:
        playlist (Playlist): The playlist to which random songs are being added.
        admin_songs (QuerySet): The queryset of admin's songs to select random songs from.
    """
    try:
        song_count = admin_songs.count()
        if song_count == 0:
            raise ValueError("No songs available to add to the playlist.")

        # Generate a list of indices to sample from
        sampling = set(random.sample(list(range(song_count)), k=min(10, song_count)))

        # Shuffle indices to ensure randomness
        order = list(range(song_count))
        random.shuffle(order)

        # Add selected songs to the playlist
        for i in range(song_count):
            if order[i] in sampling:
                relation = Playlist_songs(playlist=playlist, song=admin_songs[order[i]])
                relation.save()

    except ValueError as e:
        # Specific error for expected operational issues, like no songs available
        raise ValueError(f"Error while adding songs: {e}")

    except IndexError as e:
        # This can occur if the random sampling index is out of range
        raise ValueError(f"Index error during song selection: {e}")

    except Exception as e:
        # General catch-all for any other unexpected exceptions
        raise ValueError(f"An unexpected error occurred while adding random songs to the playlist: {e}")


def detect_emotion(request: HttpRequest):
    """
    Detects emotion from the user's image and processes the result.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Tuple[str, Any]: A tuple containing the redirect destination and any additional arguments.
    """
    try:
        # Retrieve the model paths and image path
        model_json_path, model_weights_path = get_model_paths()
        img_path = get_image_path(request)

        # Initialize the facial expression model
        face_expression = emotion_model.FacialExpressionModel(model_json_path, model_weights_path, img_path)

        # Retrieve and delete the image from the database
        image = Image.objects.get(user=request.user)
        image.delete()

        # Preprocess the image and detect emotion
        return_val, processed_img = face_expression.preprocess_img()
        print(return_val, processed_img)

        # Process the return value to decide the next steps
        return process_return_val(request, return_val, processed_img, face_expression)

    except ValueError as e:
        # Handle expected value errors, such as invalid paths or missing data
        raise ValueError(f"An error occurred: {e}")

    except Exception as e:
        # General catch-all for any other unexpected exceptions
        raise ValueError(f"An unexpected error occurred while detecting emotion: {e}")


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
    try:

        print(return_val)
        # Default error handling setup
        to, args = 'error-page', "Some error"

        # Process based on the type of detection result
        if return_val == "noFace":
            to, args = "error-page", "No Face detected for given image, try again with a new image."
        elif return_val == "mulFace":
            to, args = "error-page", "Multiple Faces detected for given image, try again with a new image."
        elif return_val == "exception":
            to, args = "error-page", "An Unknown Error Occurred, Please Try Again."

        # Check if emotion detection was successful and take action
        emotion = ""
        if return_val:
            success = face_expression.predict_emotion(processed_img)
            if success:
                emotion = face_expression.get_emotions()
                print(f'Emotion: {emotion}')
                playlist_id = create_playlist(request, emotion)
                to, args = 'displayPlaylist', playlist_id

        return to, args

    except AttributeError as e:
        # Handles issues related to attribute accesses
        raise ValueError(f"Attribute error occurred: {e}")

    except Exception as e:
        # General catch-all for any other unexpected exceptions
        raise ValueError(f"An unexpected error occurred during the processing of the return value: {e}")


def get_playlist_from_emotion(request) -> Union[redirect]:
    """
    Predict emotion from the user's image and create a playlist accordingly.

    Args:
        request: The HTTP request object.

    Returns:
        Union[redirect]: Redirects to the error page if an error occurs, otherwise redirects to the display playlist page.
    """
    try:
        # Call the emotion detection function which also processes the result
        to, args = detect_emotion(request)

        print(to, args)

        # Redirect based on the outcome of the emotion detection and processing
        return redirect(to, args)

    except ValueError as e:
        # Handle specific errors potentially thrown by the detect_emotion function
        print(f"Error processing emotion detection: {e}")
        return redirect('error-page', message="An error occurred while processing your request.")

    except Exception as e:
        # General catch-all for any other unexpected exceptions
        print(f"Unhandled error: {e}")
        return redirect('error-page', message="An unexpected error occurred.")
