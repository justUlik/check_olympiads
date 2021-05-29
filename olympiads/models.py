"""
Models for olympiad information
"""
from django.db import models
from django.contrib.auth.models import User
from autorization.models import Profile

class Olympiad(models.Model):
    """
    Descriptioning fields of Olympiad model
    """
    CHOICES_RANKS = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("н", "нет"),
    ]
    CHOICES_SUBJECT = [
        ("Математика", "Математика"),
        ("Русский язык", "Русский язык"),
        ("Литература", "Литература"),
        ("История", "История"),
        ("Физическая культура", "Физическая культура"),
        ("Музыка", "Музыка"),
        ("Технология", "Технология"),
        ("Химия", "Химия"),
        ("Биология", "Биология"),
        ("Физика", "Физика"),
        ("Экология", "Экология"),
        ("География", "География"),
        ("Естествознание", "Естествознание"),
        ("Астрономия", "Астрономия"),
        ("Окружающий мир", "Окружающий мир"),
        ("Изобразительное искусство", "Изобразительное искусство"),
        ("Основы безопасности жизнедеятельности", "Основы безопасности жизнедеятельности"),
        ("Информатика", "Информатика"),
        ("Робототехника", "Робототехника"),
        ("Экономика", "Экономика"),
    ]
    subject = models.TextField(choices=CHOICES_SUBJECT, max_length=100, blank=True)
    name = models.TextField(max_length=100, blank=True)
    register_end_date = models.DateField(default=None)
    competition_date = models.DateField(default=None)
    description = models.TextField(max_length=1000, blank=True)
    rank = models.TextField(choices=CHOICES_RANKS)
    support_email = models.EmailField(default=None)
    address = models.TextField(default=None)


    def __str__(self):
        return str(self.name)

class registerOlympiad(models.Model):
    """
    Descriptioning fields of registerOlympiad model
    """
    olympiad = models.OneToOneField(Olympiad, on_delete=models.CASCADE, related_name='register_Olympiad', default=None)
    usr = models.OneToOneField(User, on_delete=models.CASCADE, related_name='participant')
    usr_profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='participant_profile')

    def __str__(self):
        return str(self.olympiad.name) + ", участник: " + str(self.usr_profile.second_name) + str(self.usr_profile.first_name)[0] + str(self.usr_profile.father_name)[0]
