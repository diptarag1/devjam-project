from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from user import views as user_views
from user.views import ProfileDetailView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Post.urls')),
    path('register/',user_views.register, name = 'register'),
    path('login/',auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name = 'logout'),
    # path('profile/',user_views.profile, name = 'profile'),
    path('user/',include('user.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
