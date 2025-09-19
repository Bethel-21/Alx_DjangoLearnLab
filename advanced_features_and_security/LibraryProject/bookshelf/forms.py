# LibraryProject/bookshelf/forms.py
from django import forms

class ExampleForm(forms.Form):
    # Add at least one field so it’s a valid form
    name = forms.CharField(max_length=100)
