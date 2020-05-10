from django.urls import reverse
from django.http import HttpResponse, JsonResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Profile
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProfileForm,UserRegisterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, DeleteView, CreateView, UpdateView)
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin

# Create your views here.
def index(request):
    return render(request,'index.html')


def register(request):
	if request.method =='POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			username = form.cleaned_data.get('username')
			# messages.success(request, f'{ username }')
			return redirect('/login')
	else:
		form = UserRegisterForm()
	return render(request, 'user/registration/register.html', {'form': form})

def userdetail(request, slug):
    userd = User.objects.filter(username__iexact=slug)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile', slug=slug)

    else:
        form = ProfileForm(instance=request.user.userprofile)
    context = {
        'users': userd[0],
        'pform': form
    }
    return render(request, "user/profile.html", context)
