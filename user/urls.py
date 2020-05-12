from django.urls import path
from . import views

urlpatterns=[
 path('<slug:slug>/profile/',views.profile,name='profile'),
 path('<slug:slug>/profile/', views.ProfileDetailView.as_view(), name='profile-other'),
 path('notifications/',views.notification,name='notifications')
]
