from django import forms
from .models import Channel

class ChannelCreateForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ['name']
