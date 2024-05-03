from typing import Any
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View, FormView

from .forms import AddPostForm, UploadFileForm

from .models import Category, Women

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


class WomenHome(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    extra_context = {"title": "Главная страница", "menu": menu, "cat_selected": 0}

    def get_queryset(self):
        return Women.published.all().select_related("cat")


class AddPage(FormView):
    form_class = AddPostForm
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    extra_context = {"title": "Добавление статьи", "menu": menu}

    def form_valid(self, form):
        print(form.cleaned_data)
        form.save()
        return super().form_valid(form)
    

def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fl = UploadFileForm(file=form.cleaned_data["file"])
            fl.save()
    else:
        form = UploadFileForm()

    return render(
        request, "women/about.html", {"title": "О сайте", "menu": menu, "form": form}
    )


class WomenCategory(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related(
            "cat"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Категория: " + self.kwargs["cat_slug"]
        context["menu"] = menu
        context["cat_selected"] = self.kwargs["cat_slug"]
        return context


class ShowPost(DetailView):
    # model = Women
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["post"].title
        context["menu"] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class TagPostList(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_contex_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Тег: " + self.kwargs["tag_slug"]
        context["menu"] = menu
        context["cat_selected"] = None
        return context

    def get_queryset(self):
        return Women.published.filter(
            tags__slug=self.kwargs["tag_slug"]
        ).select_related("cat")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk)

    data = {
        "title": f"Рубрика: {category.name}",
        "menu": menu,
        "posts": posts,
        "cat_selected": category.pk,
    }
    return render(request, "women/index.html", context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
