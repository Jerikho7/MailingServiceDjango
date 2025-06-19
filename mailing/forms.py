from django import forms
from mailing.models import Client, Message, Mailing


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


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_mailing", "end_mailing", "message", "clients"]
        widgets = {
            "start_mailing": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "end_mailing": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
        }

    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control", "placeholder": "Выберите клиентов"}),
        label="Получатели",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["status"] = forms.ChoiceField(
                choices=Mailing.STATUS_CHOICES, label="Статус", widget=forms.Select(attrs={"class": "form-select"})
            )

        if user:
            self.fields["message"].queryset = Message.objects.filter(user=user)
            self.fields["clients"].queryset = Client.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get("start_mailing")
        end = cleaned_data.get("end_mailing")

        if start and end and start >= end:
            self.add_error("end_mailing", "Дата окончания должна быть позже даты начала")

        return cleaned_data
