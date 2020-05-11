from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from Tag.models import Tag

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	views = models.ManyToManyField(User, related_name='post_views', blank = True)
	likers = models.ManyToManyField(User, related_name = 'likers', blank = True)
	tags = models.ManyToManyField(Tag, related_name = 'tags', blank = True)

	def get_absolute_url(self):
		return reverse('post-detail', kwargs = {'pk':self.pk})



class Comment(models.Model):
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, related_name = 'likes', blank = True)

	def get_absolute_url(self):
		return reverse('post-detail', kwargs = {'pk':self.post.pk})
