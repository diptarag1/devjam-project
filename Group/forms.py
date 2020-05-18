from django import forms
from .models import Channel,Group

class ChannelCreateForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ['name']

class GroupUpdateForm(forms.ModelForm):

	class Meta:
		model = Group
		fields = ['description','logo']
