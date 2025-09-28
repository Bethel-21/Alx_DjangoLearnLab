# urls.py (in your main project folder)
from django.urls import path, include
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('api/', include('api.urls')),  # Ensure this is included
    path('books/', BookListView.as_view(), name='book-list'),  # List all books or create a new one
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # Retrieve, update or delete a book by ID
    path('books/create/', BookCreateView.as_view(), name='book-create'),  # Create a new book
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),  # Update an existing book
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),  # Delete a book
]
