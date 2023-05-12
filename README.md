# Digital API library

## An API application to provide the data of the books.

### Installation

* Execute ```pip install -r requirements.txt```
* Execute ```python manage.py migrate```
* If there are no books in the database, execute ```python manage.py get_books```. This command
will create 100 new instances of the model Book, with the data taken from www.goodreads.com. Instances can be also created 
in admin panel posted in API.
* Execute ```python manage.py runserver``` to start the application.

### Basic functions

#### The library has four main links:

* /library/books/ - A list of all books
  * Accepts **get requests**
  * Can be filtered by fields *author* (author's id); *pages* (greater than or equal to / less than or equal to)
* /library/books/<int:pk>/ - Details of a selected book ("pk" is an id of the book)
  * Accepts **get / post / delete requests**
* /library/books/authors/ - A list of all authors
  * Accepts **get requests** 
  * Can be filtered by fields *first_name*; *last_name*
* /library/books/authors/<int:pk>/ -  Details of a selected author ("pk" is an id of the book)
  * Accepts **get / post / delete requests** 


More endpoints can be found at /swagger/