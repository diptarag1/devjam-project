from django import forms
from .models import GroupPost
from Tag.models import Tag
from django.forms import formset_factory,modelformset_factory
from .models import Poll,PollChoice,Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

official_tag=['official','avishkar','freshers']
class PostCreateFrom(forms.ModelForm):
	class Meta:
		model = Post
		fields=['title','tags','content']
		widgets = {
            'content': SummernoteWidget(),
        }
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user',None)
		super().__init__(*args,**kwargs)
		print(user)
		if not user.is_superuser:
			self.fields['tags'].queryset=Tag.objects.exclude(name__in=official_tag)

class PostUpdateFrom(forms.ModelForm):
	class Meta:
		model = Post
		fields=['title','tags','content']
		widgets = {
            'content': SummernoteWidget(),
        }
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user',None)
		super().__init__(*args,**kwargs)
		print(user)
		if not user.is_superuser:
			self.fields['tags'].queryset=Tag.objects.exclude(name__in=official_tag)

class PollForm(forms.ModelForm):

	class Meta:
		model = Poll
		fields = ['title']

PollChoiceFormset = modelformset_factory(
    PollChoice,
    fields=('option', ),
    extra=4,
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'enter option'
            }
        )
    }
)

class GroupPostCreateForm(forms.ModelForm):

	class Meta:
		model = GroupPost
		fields = ['title','tags','content']
		widgets = {
            'content': SummernoteWidget(),
        }
	def __init__(self,*args, **kwargs):
		users = kwargs.pop('user',None)
		super().__init__(*args,**kwargs)
		print(users)
		if not users.is_superuser:
			self.fields['tags'].queryset=Tag.objects.exclude(name__in=official_tag)

class SearchForm(forms.Form):

	SearchTerm = forms.CharField(required = True)
