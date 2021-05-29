"""
Models for user profile information
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

CHOICES = [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
]

class Profile(models.Model):
    """
    Descriptioning fields of UserProfile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, default="")
    second_name = models.CharField(max_length=50, blank=True, default="")
    father_name = models.CharField(max_length=50, blank=True, default="")
    birth_date = models.DateField(null=True, blank=True, default=None)
    grade = models.TextField(choices=CHOICES, blank=True, default="")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
