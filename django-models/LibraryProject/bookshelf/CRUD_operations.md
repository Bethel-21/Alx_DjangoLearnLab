

# CRUD Operations for Book Model

## 1. Create
```python
from bookshelf.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book

<Book: 1984 by George Orwell>

# Get all books
Book.objects.all()

# Get the first book and its fields
book = Book.objects.first()
book.title, book.author, book.publication_year

<QuerySet [<Book: 1984 by George Orwell>]>
('1984', 'George Orwell', 1949)


# Update book title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book.title

'Nineteen Eighty-Four'

# Delete the book
book.delete()

# Confirm deletion
Book.objects.all()
(1, {'bookshelf.Book': 1})
<QuerySet []>
