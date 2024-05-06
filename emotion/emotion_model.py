from tensorflow.keras.models import model_from_json, load_model
import numpy as np
import cv2


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
        with open(model_json_file, "r") as json_file:
            loaded_model_in_json = json_file.read()
            model = model_from_json(loaded_model_in_json)
            model.load_weights(model_weights_file)
        return model

    @staticmethod
    def load_image(img_file: str):
        """
        Load the image from file.

        Args:
            img_file (str): Path to the image file.

        Returns:
            numpy.ndarray: The loaded image.
        """
        return cv2.imread(img_file)

    @staticmethod
    def load_face_cascade():
        """
        Load the Haar cascade classifier for face detection.

        Returns:
            cv2.CascadeClassifier: The loaded face cascade classifier.
        """
        return cv2.CascadeClassifier("emotion/haarcascade_frontalface_default.xml")

    def preprocess_img(self):
        """
        Preprocess the image by resizing and converting to RGB format, and detecting faces.

        Returns:
            tuple: A tuple containing a boolean indicating success or failure of preprocessing
                   and the preprocessed ROI image.
        """
        self.image = self.convert_to_rgb(self.image)
        faces = self.detect_faces()
        if not faces.any():
            return "noFace", None
        elif len(faces) > 1:
            return "mulFace", None
        else:
            roi_img = self.extract_roi(faces)
            roi_img = self.resize_image(roi_img)
            roi_img = self.normalize_image(roi_img)
            return True, roi_img

    @staticmethod
    def convert_to_rgb(image):
        """
        Convert image to RGB format.

        Args:
            image: The input image.

        Returns:
            numpy.ndarray: The image in RGB format.
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def detect_faces(self):
        """
        Detect faces in the image.

        Returns:
            list: List of tuples containing coordinates (x, y, w, h) of detected faces.
        """
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        return self.face_cascade.detectMultiScale(img, 1.3, 5)

    def extract_roi(self, faces):
        """
        Extract region of interest (ROI) from the image based on detected faces.

        Args:
            faces (list): List of tuples containing coordinates (x, y, w, h) of detected faces.

        Returns:
            numpy.ndarray: The ROI image.
        """
        x, y, w, h = faces[0]
        return self.image[y:y + h, x:x + w]

    @staticmethod
    def resize_image(image):
        """
        Resize the image to a fixed size.

        Args:
            image: The input image.

        Returns:
            numpy.ndarray: The resized image.
        """
        return cv2.resize(image, (256, 256))

    @staticmethod
    def normalize_image(image):
        """
        Normalize the image pixel values.

        Args:
            image: The input image.

        Returns:
            numpy.ndarray: The normalized image.
        """
        return image / 255.0

    def predict_emotion(self, roi_img: np.ndarray) -> bool:
        """
        Predict the emotion from the preprocessed ROI image.

        Args:
            roi_img (np.ndarray): The preprocessed ROI image.

        Returns:
            bool: True if prediction is successful, False otherwise.
        """
        prediction = self.get_prediction(roi_img)
        if prediction is None:
            return False
        self.emotion_output = self.get_emotion_label(prediction)
        return True

    def get_prediction(self, roi_img: np.ndarray):
        """
        Get the emotion prediction from the model.

        Args:
            roi_img (np.ndarray): The preprocessed ROI image.

        Returns:
            np.ndarray: The prediction array if successful, None otherwise.
        """
        try:
            return self.model.predict(roi_img.reshape(1, self.IMG_SIZE, self.IMG_SIZE, 3))
        except Exception as e:
            print(f"An Error Occurred during prediction: {e}")
            return None

    @staticmethod
    def get_emotion_label(prediction: np.ndarray) -> str:
        """
        Get the emotion label from the prediction.

        Args:
            prediction (np.ndarray): The emotion prediction array.

        Returns:
            str: The predicted emotion label.
        """
        labels = ["happy", "normal", "sad"]
        return labels[np.argmax(prediction)]

    def get_emotions(self):
        """
        Get the predicted emotion.

        Returns:
            str: The predicted emotion.
        """
        return self.emotion_output
