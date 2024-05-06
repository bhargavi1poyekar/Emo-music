from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Image(models.Model):
    """
    Model representing an image uploaded by a user.

    Each image is associated with a user through a ForeignKey relationship.

    Attributes:
        user (ForeignKey): The user who uploaded the image.
        Image_url (ImageField): The URL of the uploaded image.
    """
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    Image_url = models.ImageField(upload_to='images/')

