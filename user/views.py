from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileCreateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from .models import Profile
from Post.models import Post
from Post.views import PostListView

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
def profile(request):
	if(request.method == 'POST'):
		#u_form = UserUpdateForm(request.POST, instance = request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)

		if(p_form.is_valid()):
			#u_form.save()
			p_form.save()
			messages.success(request, 'Account has been updated.')
			return redirect('profile')
	else:
		p_form = ProfileUpdateForm(instance = request.user.profile)

	context = {
		'pform':p_form
	}
	context['posts'] = Post.objects.filter(author__profile = request.user.profile)
	return render(request, 'users/profile.html', context)




class ProfileDetailView(DetailView):
	model = Profile
	template_name = 'users/profile_other.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		context['posts'] = Post.objects.filter(author__profile = self.object)
		return context
