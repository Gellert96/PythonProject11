from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Создает группу модераторов продуктов и назначает ей права."""

    help = "Создает группу «Модератор продуктов» и назначает необходимые права"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name="Модератор продуктов",
        )

        permissions = Permission.objects.filter(
            content_type__app_label="catalog",
            content_type__model="product",
            codename__in=(
                "can_unpublish_product",
                "delete_product",
            ),
        )

        group.permissions.set(permissions)

        if created:
            self.stdout.write(
                self.style.SUCCESS("Группа «Модератор продуктов» создана.")
            )
        else:
            self.stdout.write("Группа «Модератор продуктов» уже существует.")

        self.stdout.write(self.style.SUCCESS("Права группы успешно обновлены."))
