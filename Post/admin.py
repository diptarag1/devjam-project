from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment, GroupPost,Poll,PollChoice

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
# Register your models here.
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
admin.site.register(GroupPost)
admin.site.register(Poll)
admin.site.register(PollChoice)
