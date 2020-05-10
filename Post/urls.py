from django.urls import path
from . import views
from user import views as u_views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path(r'^post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path(r'^post/new/', PostCreateView.as_view(), name='post-create'),
    path(r'^post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path(r'^post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path(r'^post/<int:pk>/comment/new/', CommentCreateView.as_view(), name='post-comment'),
]
