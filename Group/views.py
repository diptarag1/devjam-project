from django.shortcuts import render, get_object_or_404 , redirect
from django.urls import reverse
from django.contrib.auth.models import User
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gmember'] = GroupMember.objects.filter(group=self.object)
        context['tags'] = Tag.objects.all
        if self.request.user in self.object.members.all():
            context['cgmember'] = get_object_or_404(GroupMember,group=self.object,user=self.request.user)
        return context

class ListGroups(ListView):
    model = Group

def addmember(request,slug):
    group = get_object_or_404(Group,slug=slug)
    try:
        GroupMember.objects.create(user=request.user,group=group)

    except IntegrityError:
        GroupMember.objects.get(user=request.user,group=group).delete()
        if(group.members.count==0):
            group.delete()
        else:
            messages.warning(request,("left successfully {}".format(group.title)))

    else:
        messages.success(request,"You are now a member of the {} group.".format(group.title))
    return redirect('group-detail',slug=slug)

def accept(request,userd,slug):
    group = get_object_or_404(Group,slug=slug)
    user = get_object_or_404(User,username=userd)
    member = GroupMember.objects.get(user=user,group=group)
    member.status = 1
    member.save()
    return redirect('group-detail',slug=slug)

def reject(request,userd,slug):
    group = get_object_or_404(Group,slug=slug)
    user = get_object_or_404(User,username=userd)
    print(user.username)
    GroupMember.objects.get(user=user,group=group).delete()
    return redirect('group-detail',slug=slug)

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
