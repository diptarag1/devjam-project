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
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse
from Tag.models import Tag
from .models import Group, GroupMember, Channel
from Post.models import GroupPost
from .forms import ChannelCreateForm


class CreateGroup(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['title','tags','description']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


def SingleGroup(request, slug, activechannel):
    group = Group.objects.filter(slug=slug).first()
    achannel = Channel.objects.filter(parentgroup = group, name = activechannel).first()
    channelform = ChannelCreateForm(request.POST)
    if(channelform.is_valid()):
        channelform.instance.parentgroup = group
        channelform.save()
        messages.success(request, f'Channel created')
        return redirect(group.get_channel_url(channelform.instance.name))
    context = {
        'gmember' : GroupMember.objects.filter(group=group).filter(status=0),
        'tags': Tag.objects.all,
        'channels' : Channel.objects.filter(parentgroup = group),
        'group' : group,
        'activechannel' : achannel,
        'countmem': GroupMember.objects.filter(group=group).filter(status=1).order_by('auth'),
        'channelform' : channelform,
    }
    if request.user in group.members.all() and request.user.is_authenticated:
        context['cgmember'] = get_object_or_404(GroupMember,group=group,user=request.user)
    context['posts'] = GroupPost.objects.filter(parentchannel = achannel)
    return render(request, 'Group/group_detail.html', context)




class ListGroups(ListView):
    model = Group

def addmember(request,slug):
    group = Group.objects.filter(slug=slug).first()
    try:
        GroupMember.objects.create(user=request.user,group=group)

    except IntegrityError:
        GroupMember.objects.get(user=request.user,group=group).delete()
        if(group.members.count()==0):
            group.delete()
            return redirect('blog-home')
        else:
            messages.warning(request,("left successfully {}".format(group.title)))

    #else:
        #messages.success(request,"You are now a member of the {} group.".format(group.title))
    return redirect('group-detail',slug=slug,activechannel='General')

def accept(request,userd,slug):
    group = Group.objects.filter(slug__iexact=slug).first()
    user = get_object_or_404(User,username=userd)
    member = GroupMember.objects.get(user=user,group=group)
    member.status = 1
    member.save()
    return redirect('group-detail',slug=slug,activechannel='General')

def reject(request,userd,slug):
    group = Group.objects.filter(slug=slug).first()
    user = get_object_or_404(User,username=userd)
    print(user.username)
    GroupMember.objects.get(user=user,group=group).delete()
    return redirect('group-detail',slug=slug,activechannel='General')

def promote_demote(request):
    slug = request.POST.get('slug')
    userd = request.POST.get('userd')
    choice = request.POST.get('choice')
    print(slug)
    print(userd)
    group = Group.objects.filter(slug__iexact=slug).first()
    user = get_object_or_404(User,username=userd)
    member = GroupMember.objects.get(user=user,group=group)
    if choice == '1':
        member.auth=member.auth-1
    else:
        member.auth=member.auth+1
    member.save()
    context = {
        'countmem' : GroupMember.objects.filter(group=group).filter(status=1).order_by('auth'),
        'group' : group,

    }
    if request.user in group.members.all() and request.user.is_authenticated:
        context['cgmember'] = get_object_or_404(GroupMember,group=group,user=request.user)
    if request.is_ajax():
        html = render_to_string('Group/member-list.html',context, request = request)
        return JsonResponse({'form':html})
    else:
        return HttpResponse('Meme')
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
