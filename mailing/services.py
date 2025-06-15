from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone
from .models import Mailing, MailingAttempt


def process_mailing(mailing: Mailing) -> None:
    """
    Обрабатывает отправку рассылки:
    - отправляет письмо каждому клиенту;
    - сохраняет результат в MailingAttempt;
    - меняет статус рассылки, если это первая отправка.
    """
    if mailing.status == 'completed':
        return

    if mailing.status == 'created':
        mailing.status = 'running'
        mailing.save(update_fields=['status'])

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
                mailing=mailing,
                status='success',
                server_response='OK',
                attempted_at=timezone.now()
            )
        except BadHeaderError as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status='fail',
                server_response=f"BadHeaderError: {str(e)}",
                attempted_at=timezone.now()
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status='fail',
                server_response=str(e),
                attempted_at=timezone.now()
            )
