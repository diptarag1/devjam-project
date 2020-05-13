from django.urls import path
from . import views
from user import views as u_views

urlpatterns=[
    path('create/',views.CreateGroup.as_view(),name='create_group'),
    path('info/<slug:slug>/',views.SingleGroup.as_view(),name='group-detail'),
    # url(r"^$", views.ListGroups.as_view(), name="all"),
    # url(r"^new/$", views.CreateGroup.as_view(), name="create"),
    # url(r"^posts/in/(?P<slug>[-\w]+)/$",views.SingleGroup.as_view(),name="single"),
    # url(r"join/(?P<slug>[-\w]+)/$",views.JoinGroup.as_view(),name="join"),
    # url(r"leave/(?P<slug>[-\w]+)/$",views.LeaveGroup.as_view(),name="leave"),
]