from django.db import models


class Author(models.Model):
    """
    Model Author. Describes the instance of an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    author_link = models.CharField(max_length=100, default='None')

    def __str__(self) -> str:
        """
        Returns first name and last name of the author
        """
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    """
    Model Book. Describes the instance of a book. Related (many-to-one) with Author.
    """
    title = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    pages = models.PositiveIntegerField()
    isbn = models.CharField(max_length=20, blank=True, null=True)
    author = models.ForeignKey(to=Author, on_delete=models.PROTECT)
    book_link = models.CharField(max_length=100, default='None')

    def __str__(self) -> models.CharField:
        """
        Returns the title of the book
        """
        return self.title
