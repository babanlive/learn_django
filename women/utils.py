menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


class DataMixin:
    paginate_by = 3
    title_page = None
    cat_selected = None

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context["title"] = self.title_page

        if self.cat_selected is not None:
            context["cat_selected"] = self.cat_selected

        if "paginator" in context:
            context["page_range"] = context["paginator"].get_elided_page_range(
                context["page_obj"].number, on_each_side=2, on_ends=1
            )

        context.update(kwargs)

        if "menu" not in context:
            context["menu"] = menu

        return context
