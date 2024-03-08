from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from . import serializers
from . import models
from rest_framework import generics
from .models import user_model


# Create your views here.
@extend_schema_view(
        list=extend_schema(summary="list of all users"),
        create=extend_schema(summary="create a user")
        )
class UserList(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = user_model.objects.all().order_by("-id")

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.UserSerializer
        elif self.action == "create":
            return serializers.CreateUserserializer


@extend_schema_view(
        retrieve=extend_schema(summary="user detail"),
        update=extend_schema(summary="edit user details")
        )
class UserDetail(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = user_model.objects.all()
    lookup_field = "username"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.UserSerializer
        elif self.action == "update":
            return serializers.EditUserSerializer


@extend_schema_view(
        list=extend_schema(summary="item list"),
        create=extend_schema(summary="create an item"),
        )
class ItemList(viewsets.ModelViewSet):
    queryset = models.Item.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ItemSerializer
        elif self.action == "create":
            return serializers.CreateItemSerializer


@extend_schema_view(
        retrieve=extend_schema(summary="item detail"),
        update=extend_schema(summary="edit item details"),
        )
class ItemDetail(viewsets.ModelViewSet):
    serializer_class = serializers.ItemSerializer
    queryset = models.Item.objects.all()
    lookup_field = "name"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.ItemSerializer
        elif self.action == "update":
            return serializers.EditItemSerializer


@extend_schema_view(
        get=extend_schema(summary="list of categories"),
        create=extend_schema(summary="create a category")
        )
class CategoryList(generics.ListCreateAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all().order_by("id")


@extend_schema_view(
        get=extend_schema(summary="category detail"),
        update=extend_schema(summary="edit category details")
        )
class CategoryDetail(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    lookup_field = "name"


@extend_schema_view(
        get=extend_schema(summary="list of items of a user"),
        )
class UserItems(generics.ListAPIView):
    lookup_field = "username"
    serializer_class = serializers.ItemSerializer

    def get_queryset(self):
        username = self.kwargs.get("username")
        queryset = models.Item.objects.filter(owner__username=username)
        return queryset


@extend_schema_view(
        get=extend_schema(summary="list of items of a category")
        )
class CategoryItems(generics.ListAPIView):
    serializer_class = serializers.ItemSerializer

    def get_queryset(self):
        category_name = self.kwargs.get("name")
        queryset = models.Item.objects.filter(category__name=category_name).order_by("id")
        return queryset


@extend_schema_view(
        list=extend_schema(summary="list of books"),
        create=extend_schema(summary="create a book"),
        )
class BookList(viewsets.ModelViewSet):
    queryset = models.Book.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.BookSerializer
        elif self.action == "create":
            return serializers.CreateBookSerializer


@extend_schema_view(
        retrieve=extend_schema(summary="book detail"),
        update=extend_schema(summary="edit book details"),
        )
class BookDetail(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    lookup_field = "title"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.BookSerializer
        elif self.action == "update":
            return serializers.EditBookSerializer


@extend_schema_view(
        list=extend_schema(summary="list of genres"),
        create=extend_schema(summary="create a genre"),
        )
class GenreList(viewsets.ModelViewSet):
    queryset = models.Genre.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.GenreSerializer
        elif self.action == "create":
            return serializers.CreateGenreSerializer


@extend_schema_view(
        retrieve=extend_schema(summary="genre detail"),
        update=extend_schema(summary="edit genre details"),
        )
class GenreDetail(viewsets.ModelViewSet):
    queryset = models.Genre.objects.all()
    lookup_field = "name"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.GenreSerializer
        elif self.action == "update":
            return serializers.GenreSerializer


@extend_schema_view(
        list=extend_schema(summary="list of books of a genre")
        )
class GenreBookList(generics.ListAPIView):
    serializer_class = serializers.BookSerializer

    def get_queryset(self):
        genre = self.kwargs.get("name")
        queryset = models.Book.objects.filter(genre__name=genre).order_by("id")
        return queryset


@extend_schema_view(
        list=extend_schema(summary="list of pages of a book"),
        create=extend_schema(summary="create a page for a book"),
        )
class BookPageList(viewsets.ModelViewSet):
    def get_queryset(self):
        book_title = self.kwargs.get("title")
        queryset = models.Book.objects.get(title=book_title).pages.all().order_by("page")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.PageSerializer
        elif self.action == "create":
            return serializers.CurrentBookCreatePageSerializer


@extend_schema_view(
        retrieve=extend_schema(summary="page detail of a book"),
        update=extend_schema(summary="edit page details of a book"),
        )
class BookPageDetail(viewsets.ModelViewSet):
    serializer_class = serializers.PageSerializer
    queryset = models.Page.objects.all()
    lookup_field = "page_number"

    def get_object(self):
        queryset = self.get_queryset()
        book_title = self.kwargs.get("title")
        page_number = self.kwargs.get("page_number")

        obj = get_object_or_404(
                queryset,
                book__title=book_title,
                page=page_number,
                )
        return obj


@extend_schema_view(
        list=extend_schema(summary="list of pages"),
        create=extend_schema(summary="create a page")
        )
class PageList(viewsets.ModelViewSet):
    queryset = models.Page.objects.all().order_by("page")

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.PageSerializer
        elif self.action == "create":
            return serializers.CreatePageSerializer


@extend_schema_view(
        retrieve=extend_schema(summary="page detail"),
        update=extend_schema(summary="edit page details")
        )
class PageDetail(viewsets.ModelViewSet):
    queryset = models.Page.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.PageSerializer
        elif self.action == "update":
            return serializers.UpdatePageSerializer
