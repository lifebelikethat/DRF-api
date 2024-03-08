from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower
from django.contrib.auth import get_user_model
user_model = get_user_model()


class Item(models.Model):
    owner = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name="items", blank=True, null=True)
    name = models.CharField(max_length=200, unique=True,)
    description = models.CharField(max_length=200)
    category = models.ManyToManyField("Category", related_name="item", blank=True)
    is_cleaned = False

    def __str__(self):
        return self.name

    def clean(self):
        self.is_cleaned = True
        if len(self.description) > 201:
            raise ValidationError("description must be 200 characters max")
        super(Item, self).clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super(Item, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ManyToManyField(user_model, related_name="books")
    description = models.CharField(max_length=200)
    genre = models.ManyToManyField("genre", related_name="book", blank=True)
    published = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


def exempt_zero(value):
    if value <= 0:
        raise ValidationError("page must be >= 0")


class Page(models.Model):
    page = models.PositiveIntegerField(validators=[exempt_zero])
    book = models.ForeignKey(Book, related_name="pages", on_delete=models.CASCADE)
    content = models.TextField(max_length=512)

    def increment_pages(self, starting_page):
        for page in models.Page.objects.all():
            if page.page >= starting_page:
                page.page += 1
                page.save()

    def save(self, *args, **kwargs):
        new_page = super(Page, self).save(*args, **kwargs)
