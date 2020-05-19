from django.urls import path
from . import views
from user import views as u_views
from Post import views as p_views

urlpatterns=[
    path('create/',views.CreateGroup.as_view(),name='create_group'),
    path('info/<slug:slug>/<activechannel>/',views.SingleGroup,name='group-detail'),
    path('add-member/<slug:slug>/',views.addmember,name='addmember'),
    path('accept/<slug:userd>/<slug:slug>',views.accept,name='accept'),
    path('reject/<slug:userd>/<slug:slug>',views.reject,name='reject'),
    path('promote_demote/$',views.promote_demote, name = 'promote_demote'),
    path('createpost/<slug:slug>/<channel>/', p_views.GroupPostCreateView, name = "group-post-create"),
    path('createpoll/<slug:slug>/<channel>/', p_views.GroupPollNew, name = "group-poll-create"),
    # path('createpoll/<slug:slug>/<channel>/', p_views.GroupPollCreateView, name = "group-poll-create"),
    path('group-list/',views.ListGroups.as_view(),name='group-list'),
]
