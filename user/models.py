from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.
SEX = ((0, "Not Defined"), (1, "Male"), (2, "Female"))


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='userprofile')
    bio = models.TextField(unique=False, default=" ")
    country = models.CharField(max_length=50, default=" ")
    gender = models.IntegerField(choices=SEX, default=0)
    # point = models.IntegerField(unique=False,default=0)

    def __str__(self):
        return self.country

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.user.username})

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
