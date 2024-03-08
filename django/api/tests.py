import datetime
from django.urls import reverse
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from . import models
from rest_framework import status
user_model = get_user_model()


# Create your tests here.
class ModelTestCase(TestCase):
    def setUp(self):
        self.user = user_model.objects.create(username="username", password="password")
        self.item = models.Item.objects.create(
                owner=self.user,
                name="laptop",
                description="my laptop description",
                )
        self.category = models.Category.objects.create(
                name="computer",
                )
        self.book = models.Book.objects.create(
                title="book1",
                description="book1 description",
                )
        self.book.author.add(self.user)
        self.genre = models.Genre.objects.create(name="genre1")
        self.page = models.Page.objects.create(
                page=1,
                book=self.book
                )

    def test_unique_item_name(self):
        with self.assertRaises(ValidationError):
            models.Item.objects.create(
                    owner=self.user,
                    name="laptop",
                    description="my laptop description",
                    )

    def test_item_category_empty(self):
        categories = list(self.item.category.all())
        self.assertEquals(categories, [])

    def test_item_charfield_length_restriction(self):
        with self.assertRaises(ValidationError):
            item = models.Item.objects.create(
                    owner=self.user,
                    name="my item",
                    description=("a" * 201)
                    )

    def test_book_unique_title(self):
        with self.assertRaises(IntegrityError):
            book = models.Book.objects.create(
                    title="book1",
                    description="my description",
                    )
            book.author.add(self.user)

    def test_book_published(self):
        self.assertEquals(type(self.book.published), datetime.date)

    def test_genre_unique_name(self):
        with self.assertRaises(IntegrityError):
            genre = models.Genre.objects.create(name="genre1")

    def test_book_genre_no_duplicate(self):
        self.book.genre.add(self.genre)
        self.book.genre.add(self.genre)
        genres_len = len(self.book.genre.all())
        self.assertEqual(genres_len, 1)

    def test_create_page(self):
        new_page = models.Page.objects.create(
                page=2,
                content="my content",
                book=self.book,
                )
        self.assertEqual(self.book.pages.last().page, 2)
        self.assertEqual(self.book.pages.last().content, "my content")
        self.assertEqual(new_page.book, self.book)


class ViewsTestCase(APITestCase):
    def setUp(self):
        self.user = user_model.objects.create(username="username", password="password")
        self.item = models.Item.objects.create(
                owner=self.user,
                name="item1",
                description="item1 description",
                )
        self.category = models.Category.objects.create(
                name="category1",
                )
        self.book = models.Book.objects.create(
                title="book1",
                description="book1 description",
                )
        self.book.author.add(self.user)
        self.genre = models.Genre.objects.create(name="genre1")
        self.page = models.Page.objects.create(
                page=1,
                content="my content",
                book=self.book,
                )

    def Test_requests(self, method, url, data={}, debug=False):
        if method == "get":
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        elif method == "put":
            response = self.client.put(url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            return response

        elif method == "post":
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            return response

        if debug is True:
            print(response.data)

    def test_UserList(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(url, {
            "username": "username1",
            "email": "a@b.com",
            "password": "password1",
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_UserDetail(self):
        url = reverse("user-detail", kwargs={"username": "username"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ItemList(self):
        url = reverse("item-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(url, {})

    def test_ItemDetail(self):
        url = reverse("item-detail", kwargs={"name": "item1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(url, {
            "name": "newitem1",
            "description": "new item1 description"
            }, format="json")

    def test_CategoryList(self):
        url = reverse("category-list")
        self.Test_requests("get", url)
        response = self.Test_requests("post", url, {"name": "category2"})
        self.assertEqual(response.data["name"], "category2")

    def test_CategoryDetail(self):
        url = reverse("category-detail", kwargs={"name": "category1"})
        self.Test_requests("get", url)
        self.Test_requests("put", url, {"name": "new category1"})

    def test_CategoryItems(self):
        url = reverse("category-items", kwargs={"name": "category1"})
        self.Test_requests("get", url)

    def test_BookList(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(url, {
            "title": "newbook1",
            "description": "newbook1 description",
            "author": 1,
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_BookDetail(self):
        url = reverse("book-detail", kwargs={"title": "book1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(url, {
            "title": "newbook1",
            "description": "newbook1 description",
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_BookPageList(self):
        url = reverse("book-page-list", kwargs={"title": "book1"})
        self.Test_requests("get", url)
        self.Test_requests("post", url, {
            "page": 2,
            "content": "my content for page 2",
            })

    def test_BookPageDetail(self):
        url = reverse("book-page-detail", kwargs={
            "title": "book1",
            "page_number": 1,
            })
        self.Test_requests("get", url)

    def test_PageList(self):
        url = reverse("page-list")
        self.Test_requests("get", url)
        self.Test_requests("post", url, {
            "page": 2,
            "content": "content for page 2",
            "book": 1,
            },)

    def test_PageDetail(self):
        url = reverse("page-detail", kwargs={"id": 1})
        self.Test_requests("get", url)

        response = self.client.put(url, {
            "page": 3,
            "content": "content for page 3"
            })
        new_page = response.data["page"]
        new_content = response.data["content"]
        self.assertEqual(new_page, 3)
        self.assertEqual(new_content, "content for page 3")

    def test_GenreList(self):
        url = reverse("genre-list")
        self.Test_requests("get", url)
        response = self.Test_requests("post", url, {"name": "genre2"})
        self.assertEqual(response.data["name"], "genre2")

    def test_GenreDetail(self):
        url = reverse("genre-detail", kwargs={"name": "genre1"})
        self.Test_requests("get", url)
        response = self.Test_requests("put", url, {"name": "new genre1"})
        self.assertEqual(response.data["name"], "new genre1")

    def test_GenreBookList(self):
        url = reverse("genre-book-list", kwargs={"name": "genre1"})
        self.Test_requests("get", url)
