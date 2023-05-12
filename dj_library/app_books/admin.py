import django.db.models
from django.contrib import admin
from .models import Book, Author
from django.http import HttpRequest


class AuthorInline(admin.TabularInline):
    """An inline for the AuthorAdmin"""
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Author Admin class, subclass of admin.ModelAdmin.
    Describes the display of the Author model in Admin Panel
    """
    list_display = 'id', 'first_name', 'last_name'
    inlines = [AuthorInline]

    def get_queryset(self, request: HttpRequest) -> django.db.models.QuerySet:
        """Returns a queryset with related books prefetched"""
        return Author.objects.prefetch_related('book_set')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Book Admin class, subclass of admin.ModelAdmin.
    Describes the display of the Book model in Admin Panel
    """
    list_display = 'id', 'title', 'author'


