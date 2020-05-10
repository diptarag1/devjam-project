from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields =('bio','country','gender')
        widgets = {
          'bio': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField()
	class Meta:
		model = User
		fields = ['username','first_name','email','password1','password2']
