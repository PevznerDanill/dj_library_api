from django.urls import path
from .views import AuthorListApiView, BookListApiView, BookDetailApiView, AuthorDetailApiView

app_name = 'app_goods'

urlpatterns = [
    path('books/', BookListApiView.as_view(), name='books'),
    path('books/<int:pk>/', BookDetailApiView.as_view(), name='book_detail'),
    path('authors/', AuthorListApiView.as_view(), name='authors'),
    path('authors/<int:pk>/', AuthorDetailApiView.as_view(), name='author_detail'),
]
