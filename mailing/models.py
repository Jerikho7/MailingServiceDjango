from django.db import models

from accounts.models import User


class Client(models.Model):
    """
    Модель клиента — получателя рассылки.
    """

    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите email")
    full_name = models.CharField(max_length=100, verbose_name="Ф.И.О. получателя", help_text="Введите Ф.И.О.")
    comment = models.TextField(
        max_length=250, null=True, blank=True, verbose_name="Комментарий", help_text="Оставьте комментарий"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clients", blank=True, null=True)

    def __str__(self):
        return f"Получатель: {self.full_name}"

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"


class Message(models.Model):
    """
    Модель сообщения для рассылки.
    """

    subject = models.CharField(max_length=100, verbose_name="Тема письма", help_text="Напишите заголовок письма")
    text = models.TextField(verbose_name="Письмо", help_text="Напишите основную часть письма")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages", blank=True, null=True)

    def __str__(self):
        return f"Письмо: {self.subject}"

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["subject"]


class Mailing(models.Model):
    """
    Модель рассылки.
    """

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("running", "Запущена"),
        ("completed", "Завершена"),
    ]

    start_mailing = models.DateTimeField(blank=True, null=True, verbose_name="Дата и время первой отправки")
    end_mailing = models.DateTimeField(blank=True, null=True, verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created", verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    clients = models.ManyToManyField(Client, verbose_name="Получатели")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mailings", blank=True, null=True)

    def __str__(self):
        return f"Рассылка #{self.id} — {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["start_mailing"]
        permissions = [
            ("can_view_all_mailings", "Может просматривать все рассылки"),
            ("can_disable_mailings", "Может отключать рассылки"),
        ]


class MailingAttempt(models.Model):
    """
    Модель попытки отправки сообщения по рассылке.
    """

    STATUS_CHOICES = [
        ("success", "Успешно"),
        ("fail", "Не успешно"),
    ]

    attempted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус")
    server_response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name="attempts", verbose_name="Рассылка")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempts", blank=True, null=True)

    def __str__(self):
        return f"Попытка #{self.id} ({self.status}) — {self.attempted_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
