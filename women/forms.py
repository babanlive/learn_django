from django import forms
from django.core.exceptions import ValidationError

from .models import Women


class AddPostForm(forms.Form):
    class Meta:
        model = Women
        fields = ["title", "slug", "content", "is_published", "cat", "husband"]
        lables = {"title": "Заголовок", "content": "Содержание"}
        widget = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 50, "rows": 7}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cat"].empty_label = "Категория не выбрана"

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 255:
            raise ValidationError("Длина превышает 255 символов")

        return title
