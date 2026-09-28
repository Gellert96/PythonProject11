from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Создает группу контент-менеджеров и назначает ей права."""

    help = "Создает группу «Контент-менеджер» и назначает права для блога"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name="Контент-менеджер",
        )

        permissions = Permission.objects.filter(
            content_type__app_label="blog",
            content_type__model="blog",
            codename__in=(
                "add_blog",
                "change_blog",
                "delete_blog",
            ),
        )

        group.permissions.set(permissions)

        if created:
            self.stdout.write(self.style.SUCCESS("Группа «Контент-менеджер» создана."))
        else:
            self.stdout.write("Группа «Контент-менеджер» уже существует.")

        self.stdout.write(self.style.SUCCESS("Права группы успешно обновлены."))
