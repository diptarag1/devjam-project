from django.urls import path
from . import views

urlpatterns=[
 path('<slug:slug>/profile/',views.profile,name='profile'),
 path('notifications/',views.notification,name='notifications')
]
