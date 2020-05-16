from django import forms
from .models import GroupPost


class GroupPostCreateForm(forms.ModelForm):

	class Meta:
		model = GroupPost
		fields = ['title','tags','content']
