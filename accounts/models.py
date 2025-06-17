from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите email")

    avatar = models.ImageField(upload_to="accounts/avatars/", blank=True, null=True, verbose_name="Аватар", help_text="Загрузите изображение")
    phone_number = PhoneNumberField(blank=True, verbose_name="Телефон", help_text="Введите номер телефона")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна", help_text="Введите страну")

    token = models.CharField(max_length=100, verbose_name="Токен", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_view_all_users", "Может просматривать всех пользователей"),
            ("can_block_users", "Может блокировать пользователей"),
            # ("can_view_all_clients")
        ]

    def __str__(self):
        return self.email

