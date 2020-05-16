from django.contrib import admin
from .models import Post, Comment, GroupPost,Poll,PollChoice

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(GroupPost)
admin.site.register(Poll)
admin.site.register(PollChoice)
