from rest_framework import serializers, pagination
from rest_framework.reverse import reverse
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from . import models
user_model = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
            view_name="user-detail",
            lookup_field="username",
            )
    items = serializers.HyperlinkedIdentityField(
            view_name="user-items",
            lookup_field="username",
            many=False,
            read_only=True,
            )
    books = serializers.HyperlinkedRelatedField(
            view_name="book-detail",
            lookup_field="title",
            many=True,
            read_only=True,
            )

    class Meta:
        model = user_model
        fields = ("url", "id", "username", "email", "items", "books", "is_staff", "is_active", "date_joined",)
        depth = 1


class CreateUserserializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ("username", "email", "password",)

    def validate(self, data):
        try:
            user = get_object_or_404(user_model, email=data["email"])
        except:
            user = None

        if user:
            raise ValidationError({"email": "email already taken"})

        return data

    def create(self, validated_data):
        user = user_model.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ("username", "email", "items",)

    def to_representation(self, instance):
        data = super(serializers.ModelSerializer, self).to_representation(instance)
        result = {"detail": "items changed"}
        return result


class EditUserItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ("items",)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
            view_name="category-detail",
            lookup_field="name",
            many=False,
            read_only=True,
            )
    items = serializers.HyperlinkedIdentityField(
            view_name="category-items",
            lookup_field="name",
            many=False,
            read_only=True,
            )

    class Meta:
        model = models.Category
        fields = ("url", "id", "name", "items",)


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
            view_name="item-detail",
            lookup_field="name",
            )
    owner = serializers.HyperlinkedRelatedField(
            view_name="user-detail",
            lookup_field="username",
            many=False,
            read_only=True,
            )
    category = serializers.HyperlinkedRelatedField(
            view_name="category-detail",
            lookup_field="name",
            many=True,
            read_only=True,
            )

    class Meta:
        model = models.Item
        fields = ("url", "id", "owner", "name", "description", "category")


class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ("name", "description", "owner", "category",)


class EditItemSerializer(serializers.ModelSerializer):
    categories = serializers.HyperlinkedRelatedField(
            view_name="category-detail",
            lookup_field="name",
            many=True,
            read_only=True,
            )

    class Meta:
        model = models.Item
        fields = ("name", "description", "category", "categories")

    def update(self, instance, validated_data):
        instance = super(EditItemSerializer, self).update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        data = super(EditItemSerializer, self).to_representation(instance)
        data.pop("category")

        for category in instance.category.all():
            data["category"].append(f"http://127.0.0.1:8000/api/categories/{category.name}/")

        return data


class BookSerializer(serializers.HyperlinkedModelSerializer):
    genre = serializers.HyperlinkedRelatedField(
            view_name="genre-detail",
            lookup_field="name",
            read_only=True,
            many=True,
            )

    url = serializers.HyperlinkedIdentityField(
            view_name="book-detail",
            lookup_field="title",
            read_only=True,
            )
    author = serializers.HyperlinkedRelatedField(
            view_name="user-detail",
            lookup_field="username",
            read_only=True,
            many=True,
            )
    pages = serializers.HyperlinkedIdentityField(
            view_name="book-page-list",
            lookup_field="title",
            read_only=True,
            many=False,
            )

    class Meta:
        model = models.Book
        fields = "__all__"


class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        exclude = ("id",)


class EditBookSerializer(serializers.ModelSerializer):
    author = serializers.CharField(required=False)

    class Meta:
        model = models.Book
        fields = "__all__"


class PageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
            view_name="page-detail",
            lookup_field="id",
            read_only=True,
            )
    book = serializers.SlugRelatedField(
            read_only=True,
            slug_field="title",
            )

    class Meta:
        model = models.Page
        fields = "__all__"


class CreatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = ("page", "book", "content",)


class CurrentBookCreatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = ("page", "content",)

    def increment_pages(self, starting_page):
        for page in models.Page.objects.all():
            if page.page >= starting_page:
                page.page += 1
                page.save()

    def create(self, validated_data):
        title = self.context.get("request").parser_context.get("kwargs").get("title")
        book = models.Book.objects.get(title=title)
        book_pages = [page_number.page for page_number in book.pages.all()]

        if validated_data.get("page") in book_pages:
            self.increment_pages(validated_data.get("page"))

        obj = models.Page.objects.create(book=book, **validated_data)
        obj.save()
        return obj


class UpdatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = ("page", "content",)

    def update(self, instance, validated_data):
        book = instance.book
        page_list = [page.page for page in instance.book.pages.all().order_by("page")]
        old_page_number = instance.page
        new_page_number = validated_data.get("page")

        if new_page_number in page_list:
            replace_page = book.pages.get(page=new_page_number)
            replace_page.page = old_page_number
            replace_page.save()

        instance = super(UpdatePageSerializer, self).update(instance, validated_data)
        return instance


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    book = serializers.HyperlinkedIdentityField(
            view_name="genre-book-list",
            lookup_field="name",
            read_only=True,
            many=False
            )

    class Meta:
        model = models.Genre
        fields = ("id", "name", "book",)


class CreateGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ("name",)


class BookGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Genre
        fields = "__all__"
