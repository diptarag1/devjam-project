from django.urls import path
from . import views
from user import views as u_views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/new/', CommentCreateView.as_view(), name='post-comment'),
    path('like/$', views.likepost, name = 'like-post'),
    path('<tag>/explore/', views.ExploreTagView, name = 'explore-tag'),
]
