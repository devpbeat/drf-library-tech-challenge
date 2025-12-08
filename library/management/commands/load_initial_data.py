from django.core.management.base import BaseCommand
from library.models import Author, Book
from datetime import date
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load initial data for Authors and Books'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading initial data...')

        # Clear existing data
        Book.objects.all().delete()
        Author.objects.all().delete()

        # Create Authors
        authors_data = [
            {
                'first_name': 'George',
                'last_name': 'Orwell',
                'birth_date': date(1903, 6, 25),
                'nationality': 'British',
                'email': 'george.orwell@example.com',
                'biography': 'English novelist, essayist, journalist and critic.'
            },
            {
                'first_name': 'Jane',
                'last_name': 'Austen',
                'birth_date': date(1775, 12, 16),
                'nationality': 'British',
                'email': 'jane.austen@example.com',
                'biography': 'English novelist known for her romantic fiction.'
            },
            {
                'first_name': 'F. Scott',
                'last_name': 'Fitzgerald',
                'birth_date': date(1896, 9, 24),
                'nationality': 'American',
                'email': 'scott.fitzgerald@example.com',
                'biography': 'American novelist and short story writer.'
            },
            {
                'first_name': 'Harper',
                'last_name': 'Lee',
                'birth_date': date(1926, 4, 28),
                'nationality': 'American',
                'email': 'harper.lee@example.com',
                'biography': 'American novelist widely known for To Kill a Mockingbird.'
            },
            {
                'first_name': 'J.K.',
                'last_name': 'Rowling',
                'birth_date': date(1965, 7, 31),
                'nationality': 'British',
                'email': 'jk.rowling@example.com',
                'biography': 'British author, best known for the Harry Potter series.'
            },
            {
                'first_name': 'Stephen',
                'last_name': 'King',
                'birth_date': date(1947, 9, 21),
                'nationality': 'American',
                'email': 'stephen.king@example.com',
                'biography': 'American author of horror, supernatural fiction, suspense, and fantasy novels.'
            },
            {
                'first_name': 'Agatha',
                'last_name': 'Christie',
                'birth_date': date(1890, 9, 15),
                'nationality': 'British',
                'email': 'agatha.christie@example.com',
                'biography': 'English writer known for her detective novels.'
            },
            {
                'first_name': 'Isaac',
                'last_name': 'Asimov',
                'birth_date': date(1920, 1, 2),
                'nationality': 'American',
                'email': 'isaac.asimov@example.com',
                'biography': 'American writer and professor of biochemistry, known for science fiction.'
            },
        ]

        authors = {}
        for author_data in authors_data:
            author = Author.objects.create(**author_data)
            authors[author.last_name] = author
            self.stdout.write(f'Created author: {author.full_name}')

        # Create Books
        books_data = [
            {
                'title': '1984',
                'isbn': '9780451524935',
                'genre': 'FICTION',
                'publication_date': date(1949, 6, 8),
                'publisher': 'Secker & Warburg',
                'page_count': 328,
                'language': 'English',
                'description': 'A dystopian social science fiction novel and cautionary tale.',
                'price': Decimal('15.99'),
                'stock_quantity': 50,
                'rating': Decimal('4.7'),
                'authors': [authors['Orwell']]
            },
            {
                'title': 'Animal Farm',
                'isbn': '9780451526342',
                'genre': 'FICTION',
                'publication_date': date(1945, 8, 17),
                'publisher': 'Secker & Warburg',
                'page_count': 112,
                'language': 'English',
                'description': 'An allegorical novella about Stalinism.',
                'price': Decimal('12.99'),
                'stock_quantity': 35,
                'rating': Decimal('4.5'),
                'authors': [authors['Orwell']]
            },
            {
                'title': 'Pride and Prejudice',
                'isbn': '9780141439518',
                'genre': 'ROMANCE',
                'publication_date': date(1813, 1, 28),
                'publisher': 'T. Egerton',
                'page_count': 432,
                'language': 'English',
                'description': 'A romantic novel of manners.',
                'price': Decimal('14.99'),
                'stock_quantity': 40,
                'rating': Decimal('4.6'),
                'authors': [authors['Austen']]
            },
            {
                'title': 'The Great Gatsby',
                'isbn': '9780743273565',
                'genre': 'FICTION',
                'publication_date': date(1925, 4, 10),
                'publisher': 'Charles Scribner\'s Sons',
                'page_count': 180,
                'language': 'English',
                'description': 'A novel about the American Dream in the Jazz Age.',
                'price': Decimal('13.99'),
                'stock_quantity': 45,
                'rating': Decimal('4.4'),
                'authors': [authors['Fitzgerald']]
            },
            {
                'title': 'To Kill a Mockingbird',
                'isbn': '9780061120084',
                'genre': 'FICTION',
                'publication_date': date(1960, 7, 11),
                'publisher': 'J. B. Lippincott & Co.',
                'page_count': 324,
                'language': 'English',
                'description': 'A novel about racial injustice in the American South.',
                'price': Decimal('16.99'),
                'stock_quantity': 30,
                'rating': Decimal('4.8'),
                'authors': [authors['Lee']]
            },
            {
                'title': 'Harry Potter and the Philosopher\'s Stone',
                'isbn': '9780439708180',
                'genre': 'FANTASY',
                'publication_date': date(1997, 6, 26),
                'publisher': 'Bloomsbury',
                'page_count': 223,
                'language': 'English',
                'description': 'The first novel in the Harry Potter series.',
                'price': Decimal('19.99'),
                'stock_quantity': 100,
                'rating': Decimal('4.9'),
                'authors': [authors['Rowling']]
            },
            {
                'title': 'The Shining',
                'isbn': '9780307743657',
                'genre': 'THRILLER',
                'publication_date': date(1977, 1, 28),
                'publisher': 'Doubleday',
                'page_count': 447,
                'language': 'English',
                'description': 'A horror novel about a family in an isolated hotel.',
                'price': Decimal('17.99'),
                'stock_quantity': 25,
                'rating': Decimal('4.3'),
                'authors': [authors['King']]
            },
            {
                'title': 'Murder on the Orient Express',
                'isbn': '9780062693662',
                'genre': 'MYSTERY',
                'publication_date': date(1934, 1, 1),
                'publisher': 'Collins Crime Club',
                'page_count': 256,
                'language': 'English',
                'description': 'A detective novel featuring Hercule Poirot.',
                'price': Decimal('14.99'),
                'stock_quantity': 20,
                'rating': Decimal('4.5'),
                'authors': [authors['Christie']]
            },
            {
                'title': 'Foundation',
                'isbn': '9780553293357',
                'genre': 'SCIENCE_FICTION',
                'publication_date': date(1951, 5, 1),
                'publisher': 'Gnome Press',
                'page_count': 255,
                'language': 'English',
                'description': 'A science fiction novel about the fall and rise of civilizations.',
                'price': Decimal('15.99'),
                'stock_quantity': 15,
                'rating': Decimal('4.4'),
                'authors': [authors['Asimov']]
            },
            {
                'title': 'Sense and Sensibility',
                'isbn': '9780141439662',
                'genre': 'ROMANCE',
                'publication_date': date(1811, 10, 30),
                'publisher': 'Thomas Egerton',
                'page_count': 409,
                'language': 'English',
                'description': 'A novel about the Dashwood sisters.',
                'price': Decimal('13.99'),
                'stock_quantity': 0,
                'rating': Decimal('4.2'),
                'authors': [authors['Austen']]
            },
        ]

        for book_data in books_data:
            authors_list = book_data.pop('authors')
            book = Book.objects.create(**book_data)
            book.authors.set(authors_list)
            self.stdout.write(f'Created book: {book.title}')

        self.stdout.write(self.style.SUCCESS(
            f'Successfully loaded {Author.objects.count()} authors and {Book.objects.count()} books'
        ))
