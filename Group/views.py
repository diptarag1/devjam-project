from django.shortcuts import render, get_object_or_404
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
        # form.instance.author = self.request.user
        return super().form_valid(form)

class SingleGroup(DetailView):
    model = Group

class ListGroups(ListView):
    model = Group


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
