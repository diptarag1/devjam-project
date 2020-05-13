from django.urls import path
from . import views
from user import views as u_views

urlpatterns=[
    path('create/',views.CreateGroup.as_view(),name='create_group'),
    path('info/<slug:slug>/<activechannel>',views.SingleGroup,name='group-detail'),
    path('add-member/<slug:slug>/',views.addmember,name='addmember'),
    path('accept/<slug:userd>/<slug:slug>',views.accept,name='accept'),
    path('reject/<slug:userd>/<slug:slug>',views.reject,name='reject'),
    # url(r"^$", views.ListGroups.as_view(), name="all"),
    # url(r"^new/$", views.CreateGroup.as_view(), name="create"),
    # url(r"^posts/in/(?P<slug>[-\w]+)/$",views.SingleGroup.as_view(),name="single"),
    # url(r"join/(?P<slug>[-\w]+)/$",views.JoinGroup.as_view(),name="join"),
    # url(r"leave/(?P<slug>[-\w]+)/$",views.LeaveGroup.as_view(),name="leave"),
]
