from django.shortcuts import render


def home(request):
    """Отображает главную страницу."""
    return render(request, "catalog/home.html")


def contacts(request):
    """Отображает страницу контактов и обрабатывает форму."""

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
