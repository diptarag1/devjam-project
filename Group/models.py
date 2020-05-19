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
    link = models.URLField(blank=True,unique=False)
    members = models.ManyToManyField(User,through="GroupMember")
    tags =models.ManyToManyField(Tag, related_name='group_tag' , blank = True)
    logo = models.ImageField(default='group_default.jpg', upload_to='group_logo')
    created_by = models.ForeignKey(User, related_name = "group_creator",on_delete = models.CASCADE, default = None, null = True)

    def get_absolute_url(self,**kwargs):
        return reverse('group-detail', kwargs={'slug':self.slug, 'activechannel' : "General"})

    def get_channel_url(self,channel,**kwargs):
        return reverse('group-detail', kwargs={'slug':self.slug, 'activechannel' : channel})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        # self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)
        if(not GroupMember.objects.filter(group = self, user = self.created_by).exists()): #creating created by user President
            GroupMember.objects.create(group = self, user = self.created_by, auth = 0, status = 1)
            c = Channel.objects.create(parentgroup = self, name = "General")               #creating groupchannel General
            d = Channel.objects.create(parentgroup = self, name = "Announcements")         #creating groupchannel Announcements upon creating of group
            c.save()
            d.save()

    def __str__(self):
        return self.title

#channel model
class Channel(models.Model):
    parentgroup = models.ForeignKey(Group, related_name = "parent_group", on_delete = models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.parentgroup.title}.{self.name}"

STATUS =((0,"Pending"),(1,"Approved"),(2,"Declined"))               #current joining status of members
AUTH =((0,"President"),(1,"Core-Members"),(2,"Elder"),(3,"Member")) #authorities of members

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,related_name="memberships")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_groups")
    status = models.IntegerField(choices=STATUS, default=0)
    auth = models.IntegerField(choices=AUTH, default=3)
    def __str__(self):
        return self.user.username +","+ self.group.title

    class Meta:
        unique_together = ("group", "user")
