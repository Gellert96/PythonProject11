from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    """Загружает тестовые данные из фикстур."""

    help = "Удаляет старые данные и загружает категории и продукты из фикстур."

    def handle(self, *args, **options) -> None:
        """Очищает таблицы и загружает тестовые данные."""

        self.stdout.write("Удаление старых данных...")

        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Загрузка категорий...")
        call_command(
            "loaddata",
            "catalog/fixtures/categories.json",
        )

        self.stdout.write("Загрузка продуктов...")
        call_command(
            "loaddata",
            "catalog/fixtures/products.json",
        )

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно загружены."))
