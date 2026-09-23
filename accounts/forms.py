from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя."""

    email = forms.EmailField(
        required=True,
        label="Электронная почта",
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "example@mail.com",
            }
        )

        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите пароль",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Повторите пароль",
            }
        )


class UserProfileForm(forms.ModelForm):
    """Форма редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "avatar",
            "phone",
            "country",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
