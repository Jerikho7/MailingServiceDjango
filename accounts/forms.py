from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

from .models import User


class UserRegisterForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, required=False, help_text="Необязательное поле. Введите номер телефона"
    )
    usable_password = None

    class Meta:
        model = User
        fields = ("email", "phone_number", "password1", "password2")

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("номер телефона должен состоять только из цифр")
        return phone_number


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

class CustomSetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']