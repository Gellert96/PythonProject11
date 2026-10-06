from django.conf import settings
from django.core.cache import cache

from catalog.models import Product


def get_products_by_category(category_id):
    """Возвращает продукты категории с использованием кеша."""

    cache_key = f"category_{category_id}"

    products = cache.get(cache_key)

    if products is None:
        products = list(
            Product.objects.filter(
                category_id=category_id,
            ).order_by("pk")
        )

        cache.set(
            cache_key,
            products,
            settings.CACHE_TTL,
        )

    return products
