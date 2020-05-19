from django import forms
from .models import Channel, Group
from Tag.models import Tag
official_tag=['official','avishkar','freshers']


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
        model=Group
        fields=['title','tags','description','logo']

    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user',None)
        super().__init__(*args,**kwargs)
        if not user.is_superuser:
            self.fields['tags'].queryset=Tag.objects.exclude(name__in=official_tag)
