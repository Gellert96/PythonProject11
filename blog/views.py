from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.models import Blog


class BlogListView(ListView):
    """Отображает список опубликованных статей."""

    model = Blog
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """Отображает одну блоговую запись."""

    model = Blog
    template_name = "blog/blog_detail.html"
    context_object_name = "blog"

    def get_object(self, queryset=None):
        blog = super().get_object(queryset)

        blog.views_count += 1
        blog.save(update_fields=["views_count"])

        return blog


class BlogCreateView(CreateView):
    """Создает новую блоговую запись."""

    model = Blog
    template_name = "blog/blog_form.html"
    fields = (
        "title",
        "content",
        "preview",
        "is_published",
    )

    def get_success_url(self):
        return reverse(
            "blog:blog_detail",
            kwargs={"pk": self.object.pk},
        )


class BlogUpdateView(UpdateView):
    """Редактирует блоговую запись."""

    model = Blog
    template_name = "blog/blog_form.html"
    fields = (
        "title",
        "content",
        "preview",
        "is_published",
    )

    def get_success_url(self):
        return reverse(
            "blog:blog_detail",
            kwargs={"pk": self.object.pk},
        )


class BlogDeleteView(DeleteView):
    """Удаляет блоговую запись."""

    model = Blog
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:blog_list")
