from django import forms
from .models import Channel, Group
from Tag.models import Tag
official_tag = ['official']


class ChannelCreateForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ['name']


class GroupUpdateForm(forms.ModelForm):

	class Meta:
		model = Group
		fields = ['description', 'logo']


class GroupCreateForm(forms.ModelForm):

	class Meta:
		model = Group
		fields = ['title', 'tags', 'description', 'logo']
