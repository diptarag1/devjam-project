from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileCreateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from .models import Profile
from Post.models import Post
from Post.views import PostListView
from django.contrib.auth.models import User

# Create your views here.
def register(request):
	if(request.method == 'POST'):
		form1 = UserRegisterForm(request.POST)
		if(form1.is_valid()):
			form1.save()
			username = form1.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}! You can now log in')
			return redirect('login')
	else:
		form1 = UserRegisterForm()
		form2 = ProfileCreateForm()
	context = {
		'form1': form1,
	}
	return render(request, 'users/register.html', context)

@login_required
def profile(request,slug):
	userd = User.objects.filter(username__iexact=slug)
	if(request.method == 'POST'):
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
		if(p_form.is_valid()):
			p_form.save()
			messages.success(request, 'Account has been updated.')
			return redirect('profile',slug=slug)
	else:
		p_form = ProfileUpdateForm(instance = request.user.profile)

	context = {
		'pform':p_form,
		'userd':userd[0],
		'slug':slug
	}
	context['posts'] = Post.objects.filter(author__profile = request.user.profile)
	return render(request, 'users/profile.html', context)




class ProfileDetailView(DetailView):
	model = Profile
	template_name = 'users/profile_other.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['posts'] = Post.objects.filter(author__profile = self.object)
		return context
