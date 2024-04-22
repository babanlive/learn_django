from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="Slug"
    )
    content = models.TextField(blank=True, verbose_name="Содержание")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
        verbose_name="Статус",
    )
    cat = models.ForeignKey(
        "Category", on_delete=models.PROTECT, verbose_name="Категория"
    )
    tags = models.ManyToManyField(
        "TagPost", blank=True, related_name="tagss", verbose_name="Теги"
    )
    husband = models.OneToOneField(
        "Husband",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="woman",
        verbose_name="Мужья",
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = "Известные женщины"
        verbose_name_plural = "Известные женщины"
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create"])]

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="Slug"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})

    def __str__(self):
        return self.name


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})

    def __repr__(self) -> str:
        return self.tag


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self) -> str:
        return self.name
