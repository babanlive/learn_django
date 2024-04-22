from typing import Any
from django.contrib import admin, messages

from .models import Category, Women


class MarriedFilter(admin.SimpleListFilter):
    title = "Статус женщины"
    parameter_name = "status"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ("married", "Замужем"),
            ("single", "Не замужем"),
        ]

    def queryset(self, request: Any, queryset: Any) -> Any:
        if self.value() == "married":
            return queryset.filter(husband__isnull=False)
        if self.value() == "single":
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ("title", "slug", "content", "cat", "husband")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    list_display = ("title", "time_create", "is_published", "cat", "brief_info")
    list_display_links = ("title",)
    ordering = ["-time_create"]
    list_editable = ("is_published",)
    list_per_page = 5
    actions = ("set_published", "set_draft")
    search_fields = ("title", "cat__ name")
    list_filter = (MarriedFilter, "cat__name", "is_published")

    @admin.display(description="краткое описание")
    def brief_info(self, women: Women):
        return f"{len(women.content)} символов"

    @admin.action(description="Опубликовать")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} статей")

    @admin.action(description="Перевести в черновик")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(
            request, f"{count} статей переведены в черновик", messages.WARNING
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
