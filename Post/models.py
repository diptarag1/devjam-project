from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from Tag.models import Tag
from Group.models import Channel

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

	def __str__(self):
		return self.title

class GroupPost(Post):
	parentchannel = models.ForeignKey(Channel, related_name = "parent_channel", on_delete=models.CASCADE)

class Comment(models.Model):
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, related_name = 'likes', blank = True)

	def get_absolute_url(self):
		return reverse('post-detail', kwargs = {'pk':self.post.pk})

class Poll(models.Model):
	title=models.CharField(max_length=100)
	# tags = models.ManyToManyField(Tag, related_name = 'tags', blank = True)

	def __str__(self):
		return self.title

class PollChoice(models.Model):
	poll = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='poll_choice')
	option = models.CharField(max_length=100,blank=True,default="")
	voters = models.ManyToManyField(User,related_name='voters')

	def __str__(self):
		return self.poll.title + self.option
