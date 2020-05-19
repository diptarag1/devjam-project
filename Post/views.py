from django.shortcuts import render, get_object_or_404 , redirect
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment ,Poll ,PollChoice
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse
from Tag.models import Tag
from .forms import PollForm,PollChoiceFormset,PostCreateFrom,GroupPostCreateForm,SearchForm,PostUpdateFrom
from Group.models import Group,Channel
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# class PostListView(ListView):
#     model = Post
#     template_name = 'Post/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tags'] = Tag.objects.all
#         context['groups'] = Group.objects.all
#         context['posts'] = Post.objects.filter(grouppost__isnull=True).annotate(like_count=Count('likers')).order_by('-like_count')
#
#         return context
official_tag=['official','avishkar','freshers']

def PostListView(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(grouppost__isnull=True).order_by('-date_posted')
    # .annotate(like_count=Count('likers')).order_by('-like_count')
        tags = Tag.objects.all
        groups = Group.objects.all
        form1 = SearchForm(request.POST)
        context = {
        'posts' : posts,
        'groups' : groups,
        'tags' : tags,
        'form' : form1,
        }
        if request.user.is_authenticated:
            aposts = posts.filter(tags__name__in=official_tag).filter(tags__in=request.user.profile.tags.all()).distinct()
            context['aposts'] = aposts
        return render(request, 'Post/home.html', context)
    else:
        return render(request,'intro.html')

class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        is_liked = False
        if (self.object.likers.filter(username = self.request.user.username).exists()):
            is_liked = True
        else:
            is_liked = False
        post = self.object
        if not self.request.user in self.object.views.all() and self.request.user.is_authenticated:
            self.object.views.add(self.request.user)
        # Add in a QuerySet of all the books
        options = PollChoice.objects.filter(poll=self.object)
        uchoice = ''
        total = 0
        for index, op in enumerate(options):
            total = total + op.voters.count()
            if self.request.user in op.voters.all():
                uchoice=op
        context['uchoice']=uchoice
        context['total']=total
        context['options']=options
        context['poll']=self.object
        context['comments'] = Comment.objects.filter(post = self.object)
        context['is_liked'] = is_liked
        context['post']  = post
        context['tags'] = post.tags.all
        return context



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateFrom

    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({'user':self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def GroupPostCreateView(request,channel,slug):
        if(request.method == 'POST'):
            form1 = GroupPostCreateForm(request.POST,user=request.user)
            if(form1.is_valid()):
                group = Group.objects.get(slug = slug)
                form1.instance.parentchannel = Channel.objects.get(parentgroup = group, name = channel)
                form1.instance.author = request.user
                form1.save()
                return redirect(group.get_channel_url(channel))
        else:
            form1 = GroupPostCreateForm(user=request.user)
        context = {
            'form': form1,
            # 'user':request.user
        }
        return render(request, 'Post/post_form.html', context)

@login_required
def commentFunc(request,pk):
    if (request.method=='POST'):
        the_content = request.POST.get('the_content')
        com=Comment(content=the_content,post=Post.objects.filter(pk = pk).first(),author=request.user)
        com.save()
        # a['job']="done"
        return HttpResponse("helo")

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostUpdateFrom

    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({'user':self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return (self.request.user == post.author)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def likepost(request):
    post = get_object_or_404(Post, id = request.POST.get('id'))
    is_liked = False
    if (post.likers.filter(username = request.user.username).exists()):
        post.likers.remove(request.user)
        is_liked = False
    else:
        post.likers.add(request.user)
        is_liked = True

    context = {
        'is_liked' : is_liked,
        'post' : post
    }
    html = render_to_string('Post/like-section.html',context, request = request)
    return JsonResponse({'form':html})

@login_required
def ExploreTagView(request, tag):
    posts = Post.objects.filter(tags__name = tag).filter(grouppost__isnull=True)
    context = {
        'posts': posts,
        'tag': tag,
    }
    return render(request, 'Post/explore-tag.html', context)

@login_required
def GroupPollNew(request,channel,slug):
    if request.method == 'GET':
        pollform = GroupPostCreateForm(request.POST,user=request.user)
        formset = PollChoiceFormset(queryset=PollChoice.objects.none())
    elif request.method == 'POST':
        pollform = GroupPostCreateForm(request.POST,user=request.user)
        formset = PollChoiceFormset(request.POST)
        if pollform.is_valid() and formset.is_valid():
            group = Group.objects.get(slug = slug)
            pollform.instance.parentchannel = Channel.objects.get(parentgroup = group, name = channel)
            pollform.instance.author = request.user
            pollform.save()
            poll = pollform.save(commit=False)
            poll.save()
            id = poll.pk
            for form in formset:
                pollob = form.save(commit=False)
                if pollob.option=='':
                    continue
                pollob.poll = poll
                pollob.save()
        return redirect(group.get_channel_url(channel))
    return render(request,'Post/poll.html',{'pollform':pollform,'formset':formset})

@login_required
def pollnew(request):
    if request.method == 'GET':
        pollform = PostCreateFrom(request.GET or None, user = request.user)
        formset = PollChoiceFormset(queryset=PollChoice.objects.none())
    elif request.method == 'POST':
        pollform = PostCreateFrom(request.POST, user = request.user)
        formset = PollChoiceFormset(request.POST)
        if pollform.is_valid() and formset.is_valid():
            poll = pollform.save(commit=False)
            poll.author = request.user
            poll.save()
            id = poll.pk
            for form in formset:
                pollob = form.save(commit=False)
                if pollob.option=='':
                    continue
                pollob.poll = poll
                pollob.save()
        return redirect('post-detail',pk=id)
    return render(request,'Post/poll.html',{'pollform':pollform,'formset':formset})

@login_required
def addpoll(request,pk,pollid):
    option = PollChoice.objects.get(pk=pk)
    option.voters.add(request.user)
    option.save()
    return redirect('post-detail',pk=pollid)

@login_required
def Search(request):
    searchstring = request.POST.get('searchterm')
    users = User.objects.filter(username__icontains = searchstring)
    groupse = Group.objects.filter(title__icontains = searchstring)
    posteys = Post.objects.filter(title__icontains = searchstring).filter(grouppost__isnull=True)
    form1 = SearchForm(request.POST)
    context = {
        'users' : users,
        'form' : form1,
        'posteys' : posteys,
        'groupse' : groupse,
    }
    html = render_to_string('Post/searchresults.html',context, request = request)
    return JsonResponse({'form':html})
