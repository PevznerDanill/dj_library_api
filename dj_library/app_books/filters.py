from django_filters import rest_framework as filters
from .models import Book


class BookFilter(filters.FilterSet):
    """
    Book Filter class, subclass of filters.FilterSet.
    Sets the fields needed for the filtering of books.
    """
    max_pages = filters.NumberFilter(field_name='pages', lookup_expr='gte')
    min_pages = filters.NumberFilter(field_name='pages', lookup_expr='lte')
    author_name = filters.AllValuesFilter(field_name='author')
    title_name = filters.AllValuesFilter(field_name='title')

    class Meta:
        model = Book
        fields = 'author_name', 'title_name', 'max_pages', 'min_pages'
