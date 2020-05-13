from django.contrib import admin
from .models import Group,GroupMember, Channel
# Register your models here.
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Channel)
