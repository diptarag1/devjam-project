from django import forms
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from PIL import Image
from Post.models import Post
from Tag.models import Tag
SEX = ((0, "Not Defined"), (1, "Male"), (2, "Female"))
official_tag=['official']
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(unique=False, default=" ")
    country = models.CharField(max_length=50, default=" ")
    regnum = models.IntegerField(default=0)
    gender = models.IntegerField(choices=SEX, default=0)
    notif = models.DateTimeField(blank=True, default=timezone.now)
    tags = models.ManyToManyField(Tag,related_name='user_tags',blank=True)
    # point = models.IntegerField(unique=False,default=0)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.user.username})

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
