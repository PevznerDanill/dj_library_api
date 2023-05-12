import bs4
import requests
from googlesearch import search
from selenium import webdriver
from time import sleep, time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dateutil.parser import parse
from datetime import datetime, timedelta, date
from selenium.common.exceptions import NoSuchElementException
from django.core.management import BaseCommand
from pprint import pprint
from app_books.models import Author, Book
from typing import Iterator, Dict


class Command(BaseCommand):
    """
    Class Command, subclass of BaseCommand.
    Creates new 100 books with data taken from www.goodreads.com
    """
    driver_path = '/Users/daniilpevzner/PycharmProjects/python_django/13_IntroductionToDjangoRESTFramework/djlibrary/app_books/management/commands/chromedriver'
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    def handle(self, *args, **options) -> None:
        """
        Starts the creation of the books.
        """
        self.stdout.write('Starting to create...\nPreparing data..\n')
        start = time()
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
        authors_and_books = self.get_books()
        time_spent = str(timedelta(seconds=time() - start))
        self.stdout.write(f'Succesfully prepared all data. '
                          f'Time spent: {time_spent} \nCreating instances...\n')

        for author_data, book_data in authors_and_books:

            new_author, result = Author.objects.get_or_create(
                first_name=author_data['first_name'],
                last_name=author_data['last_name'],
                birth_date=author_data['birth_date'],
                author_link=author_data['author_link']
            )
            new_book, result = Book.objects.get_or_create(
                title=book_data['title'],
                date=book_data['date'],
                pages=book_data['pages'],
                isbn=book_data['isbn'],
                book_link=book_data['book_link'],
                author=new_author
            )
            self.stdout.write(f'Created new book {new_book.title} by {new_author.last_name}')
        self.stdout.write(self.style.SUCCESS('Created 100 books'))

    def get_books(self) -> Iterator:
        """Gets general data of the books from www.goodreads.com"""

        url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever'

        my_req = requests.get(url)

        my_soup = bs4.BeautifulSoup(my_req.text, 'html5lib')

        my_table = my_soup.find('table', {'class': 'tableList'})

        book_items = my_table.find_all('tr')

        default_link = 'https://www.goodreads.com'

        authors_data_list = []

        books_data_list = []

        for book_index, book_item in enumerate(book_items):
            self.stdout.write(f'Starting to prepare the {book_index + 1} book')
            start = time()
            author_data = {}
            book_data = {}

            title = book_item.find('a', {'class': 'bookTitle'})
            title_str = title.find('span').text
            title_link = default_link + title.get('href')
            author = book_item.find('a', {'class': 'authorName'})

            book_data = self.get_book(title_link)
            pages = book_data['pages']
            date_published = book_data['date_pub']
            isbn = book_data['isbn']

            author_full = author.find('span', {'itemprop': 'name'}).text.split()
            author_first_name = author_full[0]
            author_last_name = ' '.join(author_full[1:])

            author_link = author.get('href')
            author_birth = self.get_author_data(author_link)

            author_data['first_name'] = author_first_name
            author_data['last_name'] = author_last_name
            author_data['birth_date'] = author_birth
            author_data['author_link'] = author_link

            book_data['title'] = title_str
            book_data['date'] = date_published
            book_data['pages'] = pages
            book_data['isbn'] = isbn
            book_data['book_link'] = title_link
            book_data['author'] = author_last_name

            authors_data_list.append(author_data)
            books_data_list.append(book_data)
            end = time()
            total = end - start
            total_str = str(timedelta(seconds=total))
            self.stdout.write(f'{book_index + 1} book done. Time spent: {total_str}\n')

        self.driver.close()
        self.driver.quit()
        return zip(authors_data_list, books_data_list)

    @classmethod
    def get_author_data(cls, url: str) -> datetime.date:
        """Gets data of the authors from a new request to www.goodreads.com"""
        my_req = requests.get(url)
        my_soup = bs4.BeautifulSoup(my_req.text, 'html5lib')
        date_b = my_soup.find('div', {'class': 'dataItem', 'itemprop': 'birthDate'})
        if date_b:
            return parse(date_b.text).date()

    def get_book(self, url: str, attempt: int = 0) -> Dict:
        """Gets specific data of the book from www.goodreads.com"""
        time_to_load = 5
        attempt = attempt
        if attempt > 0:
            time_to_load *= 2
        dict_to_return = {
            'pages': 1,
            'date_pub': date.today(),
            'isbn': '00000000000000',
        }
        try:
            self.driver.get(url)
            sleep(time_to_load)
            btn = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div[1]/div[2]/div[1]/div[2]/div[6]/div/div/button')
            self.driver.execute_script('arguments[0].click();', btn)
            sleep(2)
            page = self.driver.page_source

            my_soup = bs4.BeautifulSoup(page, 'html5lib')
            book_div_data = my_soup.find('div', {'class': 'EditionDetails'})
            book_lst_data = book_div_data.find_all('div', {'class': 'DescListItem'})
            pages_html = book_lst_data[0].find('div', {'class': 'TruncatedContent__text'})
            dict_to_return['pages'] = int(pages_html.text.split()[0])
            date_pub_html = book_lst_data[1].find('div', {'class': 'TruncatedContent__text'})
            dict_to_return['date_pub'] = parse(date_pub_html.text.split('by')[0]).date()
            isbn_html = book_lst_data[2].find('div', {'class': 'TruncatedContent__text'})
            isbn = isbn_html.text.split()[0]

            if not isbn.isdigit():
                isbn = None
            dict_to_return['isbn'] = isbn

        except NoSuchElementException:
            if attempt == 0:
                dict_to_return = self.get_book(url, attempt=1)
        finally:
            return dict_to_return

#
# start = time()
# result = get_books()
# for author_data, book_data in result:
#
#     print('\nAuthor: {first_name} {second_name}\n'.format(
#         first_name=author_data['first_name'],
#         second_name=author_data['last_name']
#     ))
#     print('Book: {title} (by {author})'.format(
#         title=book_data['title'],
#         author=book_data['author']
#     ))
#
# total_time = time() - start
# total_time_str = timedelta(seconds=total_time)
# print(f'\nTotal time spent: {total_time_str}')

