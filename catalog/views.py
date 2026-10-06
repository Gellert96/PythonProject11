from django.conf import settings
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from catalog.forms import ProductForm
from catalog.models import Category, Product
from catalog.services import get_products_by_category


class ProductListView(ListView):
    """Отображает список товаров."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.order_by("pk")


@method_decorator(
    cache_page(settings.CACHE_TTL),
    name="dispatch",
)
@method_decorator(
    vary_on_cookie,
    name="dispatch",
)
class ProductDetailView(LoginRequiredMixin, DetailView):
    """Отображает информацию об одном товаре."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создает новый товар."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
        """Назначает владельцем текущего пользователя."""

        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "product_detail",
            kwargs={"pk": self.object.pk},
        )


class ProductUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    """Редактирует товар владелец или модератор."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def test_func(self):
        product = self.get_object()

        return product.owner == self.request.user or self.request.user.has_perm(
            "catalog.can_unpublish_product"
        )

    def get_success_url(self):
        return reverse(
            "product_detail",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    """Удаляет товар владелец или модератор."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        product = self.get_object()

        return product.owner == self.request.user or self.request.user.has_perm(
            "catalog.delete_product"
        )


class ProductUnpublishView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    View,
):
    """Отменяет публикацию товара."""

    permission_required = "catalog.can_unpublish_product"
    raise_exception = True

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save(update_fields=["is_published"])

        return redirect(
            "product_detail",
            pk=product.pk,
        )


class CategoryProductListView(View):
    """Отображает продукты выбранной категории."""

    template_name = "catalog/category_products.html"

    def get(self, request, category_id):
        category = get_object_or_404(
            Category,
            pk=category_id,
        )
        products = get_products_by_category(category_id)

        return render(
            request,
            self.template_name,
            {
                "category": category,
                "products": products,
            },
        )


class ContactsView(View):
    """Отображает и обрабатывает страницу контактов."""

    template_name = "catalog/contacts.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {"success": False},
        )

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print("Получены данные формы:")
        print(f"Имя: {name}")
        print(f"Email: {email}")
        print(f"Сообщение: {message}")

        return render(
            request,
            self.template_name,
            {"success": True},
        )
