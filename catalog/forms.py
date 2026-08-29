from django import forms

from catalog.models import Product


class ProductForm(forms.ModelForm):
    """Форма для создания нового товара."""

    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "image",
            "category",
            "price",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Название товара",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Описание товара",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].required = True
        self.fields["description"].required = True
        self.fields["image"].required = True
        self.fields["category"].required = True
        self.fields["price"].required = True

    def clean_price(self):
        """Проверяет, что цена больше нуля."""

        price = self.cleaned_data["price"]

        if price <= 0:
            raise forms.ValidationError("Цена должна быть больше нуля.")

        return price
