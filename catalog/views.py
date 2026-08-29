from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from catalog.forms import ProductForm
from catalog.models import Product


def home(request):
    products = Product.objects.all()

    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "page_obj": page_obj,
    }

    return render(request, "catalog/home.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {
        "product": product,
    }

    return render(request, "catalog/product_detail.html", context)


def product_create(request):
    if request.method == "POST":
        form = ProductForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            product = form.save()

            return redirect(
                "product_detail",
                pk=product.pk,
            )
    else:
        form = ProductForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "catalog/product_form.html",
        context,
    )


def contacts(request):
    success = False

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print("Получены данные формы:")
        print(f"Имя: {name}")
        print(f"Email: {email}")
        print(f"Сообщение: {message}")

        success = True

    return render(
        request,
        "catalog/contacts.html",
        {"success": success},
    )
