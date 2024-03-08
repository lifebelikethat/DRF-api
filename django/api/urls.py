from django.urls import path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
        path('', SpectacularSwaggerView.as_view(url_name='schema')),
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('users/', views.UserList.as_view({
            'get': 'list',
            'post': 'create',
            }), name='user-list'),
        path('users/<str:username>/', views.UserDetail.as_view({
            'get': 'retrieve',
            'put': 'update',
            }), name='user-detail'),
        path('users/<str:username>/items/', views.UserItems.as_view(), name='user-items'),
        path('items/', views.ItemList.as_view({
            'get': 'list',
            'post': 'create',
            }), name='item-list'),
        path('items/<str:name>/', views.ItemDetail.as_view({
            'get': 'retrieve',
            'put': 'update',
            }), name='item-detail'),
        path('categories/', views.CategoryList.as_view(), name='category-list'),
        path('categories/<str:name>/', views.CategoryDetail.as_view(), name='category-detail'),
        path('categories/<str:name>/items/', views.CategoryItems.as_view(), name='category-items'),
        path('books/', views.BookList.as_view({
            'get': 'list',
            'post': 'create',
            }), name='book-list'),
        path('books/<str:title>/', views.BookDetail.as_view({
            'get': 'retrieve',
            'put': 'update',
            }), name='book-detail'),
        path('books/<str:title>/pages/', views.BookPageList.as_view({
            'get': 'list',
            'post': 'create',
            }), name='book-page-list'),
        path('books/<str:title>/<int:page_number>/', views.BookPageDetail.as_view({
            'get': 'retrieve',
            }), name='book-page-detail'),
        path('pages/', views.PageList.as_view({
            'get': 'list',
            'post': 'create',
            }), name='page-list'),
        path('pages/<int:id>/', views.PageDetail.as_view({
            'get': 'retrieve',
            'put': 'update',
            }), name='page-detail'),
        path('genres/', views.GenreList.as_view({
            'get': 'list',
            'post': 'create',
            }), name='genre-list'),
        path('genres/<str:name>/', views.GenreDetail.as_view({
            'get': 'retrieve',
            'put': 'update',
            }), name='genre-detail'),
        path('genres/<str:name>/books/', views.GenreBookList.as_view(), name='genre-book-list'),
        ]
