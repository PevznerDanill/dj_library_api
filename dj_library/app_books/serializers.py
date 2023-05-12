from .models import Author, Book
from rest_framework import serializers


class BookShortSerializer(serializers.ModelSerializer):
    """
    A short serializer for the model Book. Includes only title and id fields.
    Services to be displayed in a books field in author's API.
    """
    class Meta:
        model = Book
        fields = 'title', 'id',


class AuthorSerializer(serializers.ModelSerializer):
    """
    A serializer for the model Author.
    """
    books = BookShortSerializer(many=True, source='book_set', read_only=True)

    class Meta:
        model = Author
        fields = 'id', 'first_name', 'last_name', 'birth_date', 'author_link', 'books',


class BookSerializer(serializers.ModelSerializer):
    """
    A serializer for the model Book.
    """
    author = serializers.CharField(source='author.last_name', read_only=True)

    class Meta:
        model = Book
        fields = 'id', 'title', 'author', 'date', 'pages', 'isbn', 'book_link',


