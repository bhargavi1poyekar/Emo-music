from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    """
    Model representing additional user profile information.

    Each profile is associated with a user through a OneToOneField relationship.

    Attributes:
        user (OneToOneField): The user associated with the profile.
        phone_number (CharField): The phone number of the user.
        bio (CharField): The biography of the user.
    """
    # required to associate Author model with User model (Important)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    # additional fields
    phone_number = models.CharField(max_length=255, default=1)
    bio = models.CharField(default="I am new User", max_length=255)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler function to create or update user profile.

    Args:
        sender: The model class that sent the signal.
        instance: The instance of the model class that triggered the signal.
        created (bool): Indicates whether the instance was created or updated.
        **kwargs: Additional keyword arguments.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
