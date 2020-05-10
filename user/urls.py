from django.urls import path
from . import views

urlpatterns=[
 path('<slug:slug>/profile/',views.userdetail,name='profile'),
]
