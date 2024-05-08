from tensorflow.keras.models import model_from_json
import numpy as np
import cv2
import logging
import os
import json

logger = logging.getLogger(__name__)


class FacialExpressionModel(object):
    """
    Class to load a pre-trained facial expression recognition model and predict emotions from images.
    """

    emotion_output = None
    IMG_SIZE = 256

    def __init__(self, model_json_file: str, model_weights_file: str, img_file: str):
        """
        Initialize the FacialExpressionModel object.

        Args:
            model_json_file (str): Path to the JSON file containing the model architecture.
            model_weights_file (str): Path to the file containing the model weights.
            img_file (str): Path to the image file to predict emotions from.
        """
        self.model = self.load_model(model_json_file, model_weights_file)
        self.image = self.load_image(img_file)
        self.face_cascade = self.load_face_cascade()

    @staticmethod
    def load_model(model_json_file: str, model_weights_file: str):
        """
        Load the pre-trained facial expression recognition model from JSON and weights files.

        Args:
            model_json_file (str): Path to the JSON file containing the model architecture.
            model_weights_file (str): Path to the file containing the model weights.

        Returns:
            keras.Model: The loaded model.
        """

        try:
            with open(model_json_file, "r") as json_file:
                loaded_model_in_json = json_file.read()
                model = model_from_json(loaded_model_in_json)
                model.load_weights(model_weights_file)
            return model
        except json.JSONDecodeError:
            raise ValueError("The JSON file is not correctly formatted.")
        except Exception as e:
            raise ValueError(f"An error occurred while loading weights: {str(e)}")
        

    @staticmethod
    def load_image(img_file: str):
        """
        Load the image from file.

        Args:
            img_file (str): Path to the image file.

        Returns:
            numpy.ndarray: The loaded image.
        """
        try:
            image = cv2.imread(img_file)  # Ensures image is read in color mode
            if image is None:
                raise ValueError("Failed to load image. The file may be corrupted or format is not supported.")
        except Exception as e:
            raise IOError(f"An error occurred while loading the image: {str(e)}")
        return image

    @staticmethod
    def load_face_cascade():
        """
        Load the Haar cascade classifier for face detection.

        Returns:
            cv2.CascadeClassifier: The loaded face cascade classifier.
        """
        try:
            # Load the Haar cascade classifier
            face_cascade = cv2.CascadeClassifier("emotion/haarcascade_frontalface_default.xml")
            return face_cascade

        except Exception as e:
            # Generic exception for any other issues
            raise ValueError(f"An error occurred while loading the Haar cascade: {e}")

    def preprocess_img(self):
        """
        Preprocess the image by resizing and converting to RGB format, and detecting faces.

        Returns:
            tuple: A tuple containing a boolean indicating success or failure of preprocessing
                   and the preprocessed ROI image.
        """
        try:
            # Convert image to RGB
            self.image = self.convert_to_rgb(self.image)

            # Detect faces in the image
            faces = self.detect_faces()

            print(faces)

            if not faces.any():  # Check if any faces were detected
                return "noFace", None
            elif len(faces) > 1:  # Check if more than one face is detected
                return "mulFace", None
            else:
                # Extract Region of Interest (ROI), resize, and normalize it
                roi_img = self.extract_roi(faces)
                roi_img = self.resize_image(roi_img)
                roi_img = self.normalize_image(roi_img)
                return True, roi_img

        except AttributeError as e:
            # Handle errors related to method calls or property accesses
            return False, f"Attribute error: {e}"

        except Exception as e:
            # Generic catch-all for any other unexpected exceptions
            return False, f"An error occurred: {e}"

    @staticmethod
    def convert_to_rgb(image):
        """
        Convert image to RGB format.

        Args:
            image: The input image.

        Returns:
            numpy.ndarray: The image in RGB format.
        """
        try:
            # Attempt to convert the image from BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return rgb_image
        except cv2.error as e:
            # Handle errors from OpenCV specifically related to the conversion process
            raise ValueError(f"OpenCV error during conversion: {e}")
        except TypeError as e:
            # Handle errors due to incorrect type, like if `image` is not a valid input for cv2.cvtColor
            raise ValueError(f"Type error: Check if the input is a valid image array: {e}")
        except Exception as e:
            # General exception catch, if any other unexpected error occurs
            raise ValueError(f"An unexpected error occurred during RGB conversion: {e}")

    def detect_faces(self):
        """
        Detect faces in the image.

        Returns:
            list: List of tuples containing coordinates (x, y, w, h) of detected faces.
        """
        try:
            # Convert the image from BGR to RGB
            img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

            # Detect faces in the image
            faces = self.face_cascade.detectMultiScale(img, 1.3, 5)

            print(faces)
            return faces

        except cv2.error as e:
            # Handle specific OpenCV errors related to image processing
            raise ValueError(f"OpenCV error during face detection: {e}")

        except AttributeError as e:
            # Handle errors related to accessing self.face_cascade if it's not set
            raise ValueError(f"Attribute error: {e}. Check if the face_cascade is properly initialized.")

        except Exception as e:
            # Catch all other exceptions
            raise ValueError(f"An unexpected error occurred during face detection: {e}")

    def extract_roi(self, faces):
        """
        Extract region of interest (ROI) from the image based on detected faces.

        Args:
            faces (list): List of tuples containing coordinates (x, y, w, h) of detected faces.

        Returns:
            numpy.ndarray: The ROI image.
        """
        try:
            # Extract coordinates for the first detected face
            x, y, w, h = faces[0]

            # Extract the ROI from the image using these coordinates
            roi = self.image[y: y + h, x: x + w]
            print(roi)
            return roi

        except IndexError as e:
            # Handle cases where faces list is not structured correctly
            raise ValueError(f"Index error: Check the structure of the face coordinates list: {e}")

        except TypeError as e:
            # Handle cases where the input is of an incorrect type
            raise ValueError(f"Type error: Check the input types of faces and image: {e}")

        except Exception as e:
            # General exception for any other error
            raise ValueError(f"An unexpected error occurred while extracting the ROI: {e}")

    @staticmethod
    def resize_image(image):
        """
        Resize the image to a fixed size.

        Args:
            image: The input image.

        Returns:
            numpy.ndarray: The resized image.
        """
        try:
            # Attempt to resize the image to 256x256 pixels
            resized_image = cv2.resize(image, (256, 256))
            return resized_image

        except cv2.error as e:
            # Handle errors specifically from OpenCV during resizing
            raise ValueError(f"OpenCV error during resizing: {e}")

        except TypeError as e:
            # Handle errors related to incorrect type, like if `image` is not a valid image array
            raise ValueError(f"Type error: Check if the input is a valid image array: {e}")

        except Exception as e:
            # Catch any other exceptions that could occur
            raise ValueError(f"An unexpected error occurred during image resizing: {e}")

    @staticmethod
    def normalize_image(image):
        """
        Normalize the image pixel values.

        Args:
            image: The input image.

        Returns:
            numpy.ndarray: The normalized image.
        """
        try:
            # Attempt to normalize the image by dividing by 255.0
            normalized_image = image / 255.0
            return normalized_image

        except TypeError as e:
            # Handle errors related to incorrect type, like if `image` is not a valid numpy array
            raise ValueError(f"Type error: Check if the input is a valid image array: {e}")

        except ZeroDivisionError as e:
            # Although unlikely, handle any zero division errors
            raise ValueError("Zero Division Error: Attempted to divide by zero in normalization.")

        except Exception as e:
            # Catch any other unexpected exceptions
            raise ValueError(f"An unexpected error occurred during image normalization: {e}")

    def predict_emotion(self, roi_img: np.ndarray) -> bool:
        """
        Predict the emotion from the preprocessed ROI image.

        Args:
            roi_img (np.ndarray): The preprocessed ROI image.

        Returns:
            bool: True if prediction is successful, False otherwise.
        """
        try:
            # Attempt to get a prediction for the ROI image
            prediction = self.get_prediction(roi_img)
            if prediction is None:
                return False

            # Convert the prediction to an emotion label
            self.emotion_output = self.get_emotion_label(prediction)
            return True

        except TypeError as e:
            # Handle cases where roi_img might not be a numpy array or other type issues
            raise ValueError(f"Type error in prediction input: {e}")

        except AttributeError as e:
            # Handle cases where methods like get_prediction or get_emotion_label might not be implemented
            raise ValueError(f"Attribute error: Missing required methods: {e}")

        except Exception as e:
            # General catch-all for any other unexpected exceptions
            raise ValueError(f"An unexpected error occurred during emotion prediction: {e}")

    def get_prediction(self, roi_img: np.ndarray):
        """
        Get the emotion prediction from the model.

        Args:
            roi_img (np.ndarray): The preprocessed ROI image.

        Returns:
            np.ndarray: The prediction array if successful, None otherwise.
        """
        try:
            # Ensure the image is reshaped to the expected input dimensions for the model
            prepared_img = roi_img.reshape(1, self.IMG_SIZE, self.IMG_SIZE, 3)
            return self.model.predict(prepared_img)
        except Exception as e:
            raise ValueError(f"An error occurred during prediction: {e}")

    @staticmethod
    def get_emotion_label(prediction: np.ndarray) -> str:
        """
        Get the emotion label from the prediction.

        Args:
            prediction (np.ndarray): The emotion prediction array.

        Returns:
            str: The predicted emotion label.
        """
        try:
            # Define the labels corresponding to the indices of the prediction array
            labels = ["happy", "normal", "sad"]

            # Use numpy.argmax to find the index of the maximum prediction score
            max_index = np.argmax(prediction)
            return labels[max_index]

        except IndexError as e:
            # Handle cases where the labels list does not match the prediction array size
            raise ValueError(f"Index error: Prediction index out of range. {e}")

        except TypeError as e:
            # Handle cases where prediction is not an array or has incorrect type
            raise ValueError(f"Type error: Prediction input must be an array with numeric values. {e}")

        except Exception as e:
            # General catch-all for any other unexpected exceptions
            raise ValueError(f"An unexpected error occurred while getting the emotion label: {e}")

    def get_emotions(self):
        """
        Get the predicted emotion.

        Returns:
            str: The predicted emotion.
        """

        try:
            # Check if emotion_output has been set and is of correct format
            
            return self.emotion_output

        except AttributeError as e:
            # Catch attribute errors specifically related to emotion_output
            raise AttributeError(f"Attribute error: {e}")

        except Exception as e:
            # General catch-all for any other unexpected exceptions
            raise ValueError(f"An unexpected error occurred while getting the emotions: {e}")
