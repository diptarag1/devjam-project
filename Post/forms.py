from django import forms
from .models import GroupPost
from django.forms import formset_factory,modelformset_factory
from .models import Poll,PollChoice,Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class PostCreateFrom(forms.ModelForm):
	class Meta:
		model = Post
		fields=['title','tags','content']
		widgets = {
            'content': SummernoteWidget(),
        }
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
                'placeholder': 'enteroption'
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
