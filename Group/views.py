from django.shortcuts import render, get_object_or_404 , redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
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
from .forms import ChannelCreateForm,GroupUpdateForm,GroupCreateForm

#class to create group
class CreateGroup(LoginRequiredMixin, CreateView):
    model = Group
    form_class=GroupCreateForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user #assigning create_by
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({'user':self.request.user})  #adding instance of current members in **kwargs
        return kwargs

#detail view of group
@login_required
def SingleGroup(request, slug, activechannel):
    group = Group.objects.filter(slug=slug).first()
    achannel = Channel.objects.filter(parentgroup = group, name = activechannel).first()
    channelform = ChannelCreateForm(request.POST)
    if(channelform.is_valid()):                                     #if channelform is valid then assigning its group parent and saving it
        channelform.instance.parentgroup = group
        channelform.save()
        messages.success(request, f'Channel created')
        return redirect(group.get_channel_url(channelform.instance.name))
    context = {
        'gmember' : GroupMember.objects.filter(group=group).filter(status=0),#list of pending members
        'tags': Tag.objects.all,#list of tags
        'channels' : Channel.objects.filter(parentgroup = group),#list of all channels of that group
        'group' : group, #intance of group
        'activechannel' : achannel,#inctance of current channel
        'countmem': GroupMember.objects.filter(group=group).filter(status=1).order_by('auth'),#list of accepted member
        'channelform' : channelform,
        'gform' : GroupUpdateForm(instance = group)
    }
    if request.user in group.members.all() and request.user.is_authenticated:
        context['cgmember'] = get_object_or_404(GroupMember,group=group,user=request.user)#GroupMember object of current user and group
    if request.method == 'POST':
        gform = GroupUpdateForm(request.POST, request.FILES, instance = group)#form for updating group details
        if gform.is_valid():
            gform.save()
    context['posts'] = GroupPost.objects.filter(parentchannel = achannel)
    return render(request, 'Group/group_detail.html', context)

#view to show list of groups
class ListGroups(LoginRequiredMixin,ListView):
    model = Group
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

#method to join and leave group
@login_required
def addmember(request,slug):
    group = Group.objects.filter(slug=slug).first()
    try:
        GroupMember.objects.create(user=request.user,group=group) #GroupMember object of current user and group

    except IntegrityError:
        GroupMember.objects.get(user=request.user,group=group).delete()
        if(group.members.count()==0):                              #if all members leave then group will be disbanded
            group.delete()
            return redirect('blog-home')
        else:
            messages.warning(request,("left successfully {}".format(group.title)))

    return redirect('group-detail',slug=slug,activechannel='General')

#method to accept a member in a group
@login_required
def accept(request,userd,slug):
    group = Group.objects.filter(slug__iexact=slug).first() #getting object of group
    user = get_object_or_404(User,username=userd)
    member = GroupMember.objects.get(user=user,group=group) #GroupMember object of current user and group
    member.status = 1
    member.save()
    return redirect('group-detail',slug=slug,activechannel='General')

#method to reject an joining application
@login_required
def reject(request,userd,slug):
    group = Group.objects.filter(slug=slug).first()         #getting object of group
    user = get_object_or_404(User,username=userd)
    GroupMember.objects.get(user=user,group=group).delete() #GroupMember object of current user and group
    return redirect('group-detail',slug=slug,activechannel='General')

#method to promote and demote authority of group members
@login_required
def promote_demote(request):
    slug = request.POST.get('slug')
    userd = request.POST.get('userd')
    choice = request.POST.get('choice')
    print(slug)
    print(userd)
    group = Group.objects.filter(slug__iexact=slug).first() #getting object of group
    user = get_object_or_404(User,username=userd)           #getting instance of member
    member = GroupMember.objects.get(user=user,group=group) #getting object of GroupMember model
    if choice == '1':                                       #promoting demoting according to choice
        member.auth=member.auth-1
    else:
        member.auth=member.auth+1
    member.save()                                           #updating authority of member
    context = {
        'countmem' : GroupMember.objects.filter(group=group).filter(status=1).order_by('auth'), # all cuurent accepted members
        'group' : group,

    }
    if request.user in group.members.all() and request.user.is_authenticated:
        context['cgmember'] = get_object_or_404(GroupMember,group=group,user=request.user)  #GroupMember object of current user and group
    if request.is_ajax():
        html = render_to_string('Group/member-list.html',context, request = request)
        return JsonResponse({'form':html})
    else:
        return HttpResponse('Meme')
