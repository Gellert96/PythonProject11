from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import UserProfileForm, UserRegisterForm
from accounts.models import User


class RegisterView(CreateView):
    """Регистрирует нового пользователя."""

    model = User
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)

        login(
            self.request,
            self.object,
            backend="django.contrib.auth.backends.ModelBackend",
        )

        send_mail(
            subject="Добро пожаловать!",
            message=(
                "Спасибо за регистрацию в нашем интернет-магазине. "
                "Ваш аккаунт успешно создан."
            ),
            from_email=None,
            recipient_list=[self.object.email],
            fail_silently=False,
        )

        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирует профиль текущего пользователя."""

    model = User
    form_class = UserProfileForm
    template_name = "accounts/profile_form.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        return self.request.user
