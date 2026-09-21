from django import forms

from catalog.models import Product

FORBIDDEN_WORDS = (
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
)


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта."""

    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "image",
            "category",
            "price",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"

        self.fields["name"].widget.attrs["placeholder"] = "Название товара"
        self.fields["description"].widget.attrs.update(
            {
                "placeholder": "Описание товара",
                "rows": 5,
            }
        )
        self.fields["price"].widget.attrs.update(
            {
                "step": "0.01",
            }
        )

    def clean_name(self):
        """Проверяет название продукта на запрещенные слова."""

        name = self.cleaned_data["name"]
        name_lower = name.lower()

        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise forms.ValidationError(
                    f'Название содержит запрещенное слово: "{word}".'
                )

        return name

    def clean_description(self):
        """Проверяет описание продукта на запрещенные слова."""

        description = self.cleaned_data["description"]
        description_lower = description.lower()

        for word in FORBIDDEN_WORDS:
            if word in description_lower:
                raise forms.ValidationError(
                    f'Описание содержит запрещенное слово: "{word}".'
                )

        return description

    def clean_price(self):
        """Проверяет, что цена продукта не отрицательная."""

        price = self.cleaned_data["price"]

        if price < 0:
            raise forms.ValidationError("Цена продукта не может быть отрицательной.")

        return price

    def clean_image(self):
        """Проверяет формат и размер нового изображения."""

        image = self.cleaned_data.get("image")

        if not image:
            return image

        content_type = getattr(image, "content_type", None)

        if content_type is not None:
            allowed_content_types = (
                "image/jpeg",
                "image/png",
            )

            if content_type not in allowed_content_types:
                raise forms.ValidationError(
                    "Разрешены только изображения в формате JPEG или PNG."
                )

            max_size = 5 * 1024 * 1024

            if image.size > max_size:
                raise forms.ValidationError(
                    "Размер изображения не должен превышать 5 МБ."
                )

        return image
