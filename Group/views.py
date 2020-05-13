from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
# from .models import Post, Comment
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse
from Tag.models import Tag
from .models import Group, GroupMember

class CreateGroup(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['title','tags','description']

    def form_valid(self, form):
        # form.instance.members.add(self.request.user)
        # self.object.membership.add(self.request.user)
        return super().form_valid(form)

class SingleGroup(DetailView):
    model = Group

class ListGroups(ListView):
    model = Group

def addmember(request,slug):
    group = get_object_or_404(Group,slug=slug)
    try:
        GroupMember.objects.create(user=request.user,group=group)

    except IntegrityError:
        GroupMember.objects.get(user=request.user,group=group).delete()
        messages.warning(request,("left successfully {}".format(group.title)))

    else:
        messages.success(request,"You are now a member of the {} group.".format(group.title))
    return render(request,"Group/add.html")

# def addgroup(request,slug):
#       group = get_object_or_404(Group,slug=self.kwargs.get("slug"))
#       try:
#             GroupMember.objects.create(user=self.request.user,group=group)
#
#         except IntegrityError:
#             messages.warning(self.request,("Warning, already a member of {}".format(group.name)))
#
#         else:
#             messages.success(self.request,"You are now a member of the {} group.".format(group.name))
