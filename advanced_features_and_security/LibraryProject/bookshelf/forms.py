# LibraryProject/bookshelf/forms.py
from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        # Include the fields you want users to be able to fill
        fields = ['title', 'author', 'published_date', 'isbn', 'pages']
