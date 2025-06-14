from django import forms
from mailing.models import Client, Message


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["full_name", "email", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 5}),
        }
