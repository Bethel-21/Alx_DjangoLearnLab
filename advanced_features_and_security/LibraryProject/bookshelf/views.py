from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm

# View books (requires can_view)
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# Create a new book (requires can_create)
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    return HttpResponse("Book created! (Placeholder)")  

# Edit a book (requires can_edit)
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Editing book: {book.title}")

# Delete a book (requires can_delete)
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Deleting book: {book.title}")
