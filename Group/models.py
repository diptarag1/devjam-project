from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
import misaka
from Tag.models import Tag
# Create your models here.
class Group(models.Model):
    title = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description =  models.TextField()
    members = models.ManyToManyField(User,through="GroupMember")
    tags =models.ManyToManyField(Tag, related_name='group_tag' , blank = True)

    def get_absolute_url(self,**kwargs):
        return reverse('group-detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        # self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

STATUS =((0,"Pending"),(1,"Approved"),(2,"Declined"))
AUTH =((0,"President"),(1,"Core-Members"),(2,"Elder"),(3,"Member"))

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,related_name="memberships")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_groups")
    status = models.IntegerField(choices=STATUS, default=0)
    auth = models.IntegerField(choices=AUTH, default=3)
    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("group", "user")
