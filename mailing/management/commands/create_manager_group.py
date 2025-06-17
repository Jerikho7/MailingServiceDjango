from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Создаёт группу Менеджеры с необходимыми правами'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Менеджеры')
        permissions = [
            "can_view_all_users",
            "can_block_users""",
            "can_view_all_mailings",
            "can_disable_mailings",
            "view_client",
            "can_view_all_active_mailings"
        ]
        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Разрешение {perm} не найдено'))
        self.stdout.write(self.style.SUCCESS('Группа Менеджеры создана или обновлена'))
