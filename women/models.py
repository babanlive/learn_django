from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    cat = models.ForeignKey("Category", on_delete=models.PROTECT)
    tags = models.ManyToManyField("TagPost", blank=True, related_name="tagss")
    husband = models.OneToOneField(
        "Husband", on_delete=models.SET_NULL, null=True, related_name="woman"
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create"])]

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    def __repr__(self):
        return f"Name = {self.title}, ID = {self.id}"


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})

    def __repr__(self):
        return f"Name = {self.name}, ID = {self.id}"


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})

    def __repr__(self) -> str:
        return f"{self.tag}"


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count= models.IntegerField(blank=True, default=0)

    def __repr__(self) -> str:
        return f"{self.name}"
