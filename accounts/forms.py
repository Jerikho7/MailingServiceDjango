from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

from .models import User


class UserRegisterForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, required=False, help_text="Необязательное поле. Введите номер телефона"
    )
    country = forms.CharField(
        max_length=50, required=False, help_text="Необязательное поле. Введите страну, где живете"
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
        help_text="Загрузите изображение (JPG, PNG, до 5MB)",
    )
    usable_password = None

    class Meta:
        model = User
        fields = ("email", "phone_number", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone_number"].label = "Телефон"
        self.fields["country"].label = "Страна"
        self.fields["avatar"].label = "Изображение профиля"

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("номер телефона должен состоять только из цифр")
        return phone_number

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            if avatar.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Размер файла не должен превышать 5MB.")
            if not avatar.name.lower().endswith((".jpg", ".jpeg", ".png")):
                raise forms.ValidationError("Поддерживаются только файлы JPG/JPEG/PNG")
        return avatar


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)


class CustomSetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]
