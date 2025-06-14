from django import forms
from mailing.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'email', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }