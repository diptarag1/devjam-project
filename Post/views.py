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
from Group.models import Group



class PostListView(ListView):
    model = Post
    template_name = 'Post/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all
        context['groups'] = Group.objects.all
        context['posts'] = Post.objects.filter(grouppost__isnull=True).annotate(like_count=Count('likers')).order_by('-like_count')
        return context
# def postdetail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     context = {'post': post}
#     if not request.user in post.views.all():
#         post.views.add(request.user)
#     return render(request, 'blog/post_detail.html', context)

class PostDetailView(DetailView):
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
        #
        if not self.request.user in self.object.views.all() and self.request.user.is_authenticated:
            self.object.views.add(self.request.user)
        # Add in a QuerySet of all the books
        context['comments'] = Comment.objects.filter(post = self.object)
        context['is_liked'] = is_liked
        context['post']  = post
        context['tags'] = post.tags.all
        return context



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','tags','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# class CommentCreateView(LoginRequiredMixin, CreateView):
#     model = Comment
#     fields = ['content']
#     template_name = 'Post/comment.html'
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in a QuerySet of all the books
#         context['posty'] = Post.objects.filter(pk = self.kwargs['pk']).first()
#         return context
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.instance.post=Post.objects.filter(pk = self.kwargs['pk']).first()
#         return super().form_valid(form)
def commentFunc(request,pk):
    if (request.method=='POST'):
        the_content = request.POST.get('the_content')
        com=Comment(content=the_content,post=Post.objects.filter(pk = pk).first(),author=request.user)
        com.save()
        # a['job']="done"
        return HttpResponse("helo")




class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

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


def ExploreTagView(request, tag):
    posts = Post.objects.filter(tags__name = tag).filter(grouppost__isnull=True)
    context = {
        'posts': posts,
        'tag': tag,
    }
    return render(request, 'Post/explore-tag.html', context)

def pollnew(request):
    return render(request,'Post/poll.html')

def polldetail(request,pk):
    poll = Poll.objects.get(pk=pk)
    options = PollChoice.objects.filter(poll=poll)
    uchoice = ''
    total = 0
    for index, op in enumerate(options):
        total = total + op.voters.count()
        if request.user in op.voters.all():
            uchoice=op
    context={}
    context['poll']=poll
    context['options']=options
    context['uchoice']=uchoice
    context['total']=total
    return render(request,'Post/poll_detail.html',context)

def addpoll(request,pk,pollid):
    option = PollChoice.objects.get(pk=pk)
    option.voters.add(request.user)
    option.save()
    return redirect('poll_detail',pk=pollid)


# def about(request):
#     return render(request, 'Post/about.html', {'title': 'About'})
