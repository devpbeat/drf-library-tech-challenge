from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date
from decimal import Decimal
from .models import Author, Book


class AuthorModelTest(TestCase):
    """Unit tests for Author model"""

    def setUp(self):
        self.author = Author.objects.create(
            first_name='John',
            last_name='Doe',
            birth_date=date(1980, 1, 1),
            nationality='American',
            email='john.doe@example.com',
            biography='Test biography'
        )

    def test_author_creation(self):
        """Test that an author can be created"""
        self.assertEqual(self.author.first_name, 'John')
        self.assertEqual(self.author.last_name, 'Doe')
        self.assertEqual(str(self.author), 'John Doe')

    def test_author_full_name(self):
        """Test the full_name property"""
        self.assertEqual(self.author.full_name, 'John Doe')

    def test_author_email_unique(self):
        """Test that email is unique"""
        with self.assertRaises(Exception):
            Author.objects.create(
                first_name='Jane',
                last_name='Doe',
                email='john.doe@example.com'
            )


class BookModelTest(TestCase):
    """Unit tests for Book model"""

    def setUp(self):
        self.author = Author.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com'
        )
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890',
            genre='FICTION',
            publication_date=date(2023, 1, 1),
            publisher='Test Publisher',
            page_count=200,
            language='English',
            description='Test description',
            price=Decimal('19.99'),
            stock_quantity=10,
            rating=Decimal('4.5')
        )
        self.book.authors.add(self.author)

    def test_book_creation(self):
        """Test that a book can be created"""
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(str(self.book), 'Test Book')

    def test_book_is_in_stock(self):
        """Test the is_in_stock property"""
        self.assertTrue(self.book.is_in_stock)
        self.book.stock_quantity = 0
        self.assertFalse(self.book.is_in_stock)

    def test_book_authors_relationship(self):
        """Test many-to-many relationship with authors"""
        self.assertEqual(self.book.authors.count(), 1)
        self.assertEqual(self.author.books.count(), 1)


class AuthorAPITest(APITestCase):
    """Integration tests for Author API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.author1 = Author.objects.create(
            first_name='Alice',
            last_name='Johnson',
            nationality='British',
            email='alice@example.com'
        )
        self.author2 = Author.objects.create(
            first_name='Bob',
            last_name='Williams',
            nationality='American',
            email='bob@example.com'
        )

    def test_get_authors_list(self):
        """Test retrieving list of authors"""
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_author_detail(self):
        """Test retrieving a single author"""
        url = reverse('author-detail', args=[self.author1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Alice')
        self.assertEqual(response.data['full_name'], 'Alice Johnson')

    def test_create_author(self):
        """Test creating a new author"""
        url = reverse('author-list')
        data = {
            'first_name': 'Charlie',
            'last_name': 'Brown',
            'nationality': 'Canadian',
            'email': 'charlie@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 3)

    def test_update_author(self):
        """Test updating an author"""
        url = reverse('author-detail', args=[self.author1.id])
        data = {
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'nationality': 'Australian',
            'email': 'alice@example.com'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author1.refresh_from_db()
        self.assertEqual(self.author1.nationality, 'Australian')

    def test_delete_author(self):
        """Test deleting an author"""
        url = reverse('author-detail', args=[self.author1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 1)

    def test_author_statistics(self):
        """Test author statistics endpoint"""
        # Create a book for testing
        book = Book.objects.create(
            title='Test Book',
            isbn='1234567890',
            genre='FICTION',
            publication_date=date(2023, 1, 1),
            publisher='Test Publisher',
            page_count=200,
            price=Decimal('19.99'),
            stock_quantity=10
        )
        book.authors.add(self.author1)

        url = reverse('author-statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('statistics', response.data)
        self.assertEqual(response.data['statistics']['total_authors'], 2)

    def test_search_authors(self):
        """Test searching authors"""
        url = reverse('author-list')
        response = self.client.get(url, {'search': 'Alice'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class BookAPITest(APITestCase):
    """Integration tests for Book API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(
            first_name='Test',
            last_name='Author',
            email='test@example.com'
        )
        self.book1 = Book.objects.create(
            title='Book One',
            isbn='1111111111',
            genre='FICTION',
            publication_date=date(2023, 1, 1),
            publisher='Publisher One',
            page_count=200,
            price=Decimal('19.99'),
            stock_quantity=10,
            rating=Decimal('4.5')
        )
        self.book1.authors.add(self.author)

        self.book2 = Book.objects.create(
            title='Book Two',
            isbn='2222222222',
            genre='MYSTERY',
            publication_date=date(2022, 6, 15),
            publisher='Publisher Two',
            page_count=300,
            price=Decimal('24.99'),
            stock_quantity=0,
            rating=Decimal('3.8')
        )
        self.book2.authors.add(self.author)

    def test_get_books_list(self):
        """Test retrieving list of books"""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_book_detail(self):
        """Test retrieving a single book"""
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Book One')
        self.assertTrue(response.data['is_in_stock'])

    def test_create_book(self):
        """Test creating a new book"""
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'isbn': '3333333333',
            'author_ids': [self.author.id],
            'genre': 'FANTASY',
            'publication_date': '2024-01-01',
            'publisher': 'New Publisher',
            'page_count': 250,
            'language': 'English',
            'price': '29.99',
            'stock_quantity': 15,
            'rating': '4.2'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        """Test updating a book"""
        url = reverse('book-detail', args=[self.book1.id])
        data = {
            'title': 'Book One Updated',
            'isbn': '1111111111',
            'author_ids': [self.author.id],
            'genre': 'FICTION',
            'publication_date': '2023-01-01',
            'publisher': 'Publisher One',
            'page_count': 200,
            'price': '22.99',
            'stock_quantity': 10
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Book One Updated')

    def test_delete_book(self):
        """Test deleting a book"""
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_by_genre(self):
        """Test filtering books by genre"""
        url = reverse('book-list')
        response = self.client.get(url, {'genre': 'FICTION'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_stock(self):
        """Test filtering books by stock availability"""
        url = reverse('book-list')
        response = self.client.get(url, {'in_stock': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_price_range(self):
        """Test filtering books by price range"""
        url = reverse('book-list')
        response = self.client.get(url, {'min_price': '20', 'max_price': '25'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_book_statistics(self):
        """Test book statistics endpoint with aggregations"""
        url = reverse('book-statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('overall_statistics', response.data)
        self.assertIn('statistics_by_genre', response.data)
        self.assertEqual(response.data['overall_statistics']['total_books'], 2)

    def test_top_rated_books(self):
        """Test top rated books endpoint"""
        url = reverse('book-top-rated')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        """Test searching books"""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Book One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_isbn_validation(self):
        """Test ISBN validation in serializer"""
        url = reverse('book-list')
        data = {
            'title': 'Invalid Book',
            'isbn': 'invalid',
            'author_ids': [self.author.id],
            'genre': 'FICTION',
            'publication_date': '2024-01-01',
            'publisher': 'Test',
            'page_count': 100,
            'price': '10.00',
            'stock_quantity': 5
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
