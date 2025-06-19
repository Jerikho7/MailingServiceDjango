from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone
from .models import MailingAttempt
from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailing.models import Mailing, Client, Message


def process_mailing(mailing: Mailing) -> None:
    """
    Обрабатывает отправку рассылки:
    - отправляет письмо каждому клиенту;
    - сохраняет результат в MailingAttempt;
    - меняет статус рассылки, если это первая отправка.
    """
    if mailing.status == "completed":
        return

    if mailing.status == "created":
        mailing.status = "running"
        mailing.save(update_fields=["status"])

        # Отправка письма каждому клиенту
        for client in mailing.clients.all():
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.text,
                    from_email=None,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=mailing, status="success", server_response="OK", attempted_at=timezone.now()
                )
            except BadHeaderError as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status="fail",
                    server_response=f"BadHeaderError: {str(e)}",
                    attempted_at=timezone.now(),
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing, status="fail", server_response=str(e), attempted_at=timezone.now()
                )


def get_clients_from_cache():
    if not CACHE_ENABLED:
        return Client.objects.all()
    key = "client_list"
    clients = cache.get(key)
    if clients:
        return clients
    clients = Client.objects.all()
    cache.set(key, clients)
    return clients


def get_messages_from_cache():
    if not CACHE_ENABLED:
        return Message.objects.all()
    key = "message_list"
    messages = cache.get(key)
    if messages:
        return messages
    messages = Message.objects.all()
    cache.set(key, messages)
    return messages


def get_mailings_from_cache():
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = "mailing_list"
    mailings = cache.get(key)
    if mailings:
        return mailings
    mailings = Mailing.objects.all()
    cache.set(key, mailings)
    return mailings
