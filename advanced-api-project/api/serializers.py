from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

# Book Serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']  # Include all fields of the Book model

    # Custom validation for publication_year to ensure it is not in the future
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("The publication year cannot be in the future.")
        return value

# Author Serializer
class AuthorSerializer(serializers.ModelSerializer):
    # Nested BookSerializer to include related books dynamically
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Include the author's name and the nested books
