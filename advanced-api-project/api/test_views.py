

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book
from django.contrib.auth.models import User


class BookAPITests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        # Create a test book
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publication_year=2024
        )

        self.book_list_url = reverse('book-list')
        self.book_detail_url = reverse('book-detail', args=[self.book.id])
        self.book_create_url = reverse('book-create')
        self.book_update_url = reverse('book-update', args=[self.book.id])
        self.book_delete_url = reverse('book-delete', args=[self.book.id])

    def test_get_books(self):
        """Test listing all books"""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_book(self):
        """Test creating a new book"""
        data = {"title": "New Book", "author": "New Author", "publication_year": 2025}
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        """Test updating an existing book"""
        data = {"title": "Updated Title", "author": "Test Author", "publication_year": 2024}
        response = self.client.put(self.book_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book(self):
        """Test deleting a book"""
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)



    def test_filter_books_by_author(self):
        """Test filtering books by author"""
        response = self.client.get(self.book_list_url, {'author': 'Test Author'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['author'], 'Test Author')

    def test_search_books_by_title(self):
        """Test searching books by title"""
        response = self.client.get(self.book_list_url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Book', response.data[0]['title'])

    def test_order_books_by_year(self):
        """Test ordering books by publication_year"""
        Book.objects.create(title="Older Book", author="Author B", publication_year=1999)
        response = self.client.get(self.book_list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 1999)
