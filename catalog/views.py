from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from catalog.forms import ProductForm
from catalog.models import Product


class ProductListView(ListView):
    """Отображает список товаров."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    """Отображает информацию об одном товаре."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """Создает новый товар."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return reverse(
            "product_detail",
            kwargs={"pk": self.object.pk},
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
