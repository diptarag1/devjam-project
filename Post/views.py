from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse
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
        context['posts'] = Post.objects.filter(grouppost__isnull=True)
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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'Post/comment.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['posty'] = Post.objects.filter(pk = self.kwargs['pk']).first()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post=Post.objects.filter(pk = self.kwargs['pk']).first()
        return super().form_valid(form)


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
#
#
# def about(request):
#     return render(request, 'Post/about.html', {'title': 'About'})
