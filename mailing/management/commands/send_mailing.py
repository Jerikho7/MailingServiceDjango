from django.core.management.base import BaseCommand
from mailing.models import Mailing
from mailing.services import process_mailing

class Command(BaseCommand):
    help = "Отправляет рассылку по ID"

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int)

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']
        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            self.stderr.write(self.style.ERROR("Рассылка не найдена"))
            return

        process_mailing(mailing)
        self.stdout.write(self.style.SUCCESS("Рассылка отправлена"))
