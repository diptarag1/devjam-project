from django import forms
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from Post.models import Post
SEX = ((0, "Not Defined"), (1, "Male"), (2, "Female"))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
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