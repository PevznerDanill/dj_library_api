from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import (
    ListModelMixin,
)
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter
from rest_framework.response import Response
from django.http import HttpRequest


class AuthorListApiView(ListModelMixin, GenericAPIView):
    """
    View class for displaying a list API for the model Author.
    """
    queryset = Author.objects.prefetch_related('book_set').all()
    serializer_class = AuthorSerializer
    filterset_fields = 'first_name', 'last_name'

    def get(self, request: HttpRequest) -> Response:
        """
        A get method for the API list for the model Author.
        """
        return self.list(request)


class AuthorDetailApiView(RetrieveUpdateDestroyAPIView):
    """
    View API class for displaying details of a selected instance of the model Author.
    """
    queryset = Author.objects.prefetch_related('book_set').all()
    serializer_class = AuthorSerializer

    def get(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        A get method to retrieve a selected instance of the model Author.
        """
        return super().retrieve(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        A post method to update the data of a selected instance of the model Author.
        """
        return super().update(request, *args, **kwargs)

    def delete(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        A delete method to delete a selected instance of the model Author.
        """
        return super().destroy(request, *args, **kwargs)


class BookListApiView(ListModelMixin, GenericAPIView):
    """
    A view API class for displaying a list of instances of the model Book.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    filterset_class = BookFilter

    def get(self, request: HttpRequest) -> Response:
        """
        A get method to retrieve a list of all the existing instances of the model Book.
        """
        return self.list(request)


class BookDetailApiView(RetrieveUpdateDestroyAPIView):
    """
    A view API class for displaying details of a selected instance of the model Book
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer

    def get(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        A get method to retrieve a selected instance of the model Book.
        """
        return super().retrieve(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        A post method to update the data of a selected instance of the model Book.
        """
        return super().update(request, *args, **kwargs)

    def delete(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        A delete method to delete a selected instance of the model Book.
        """
        return super().destroy(request, *args, **kwargs)
