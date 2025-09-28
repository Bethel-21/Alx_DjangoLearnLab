from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class AuthorSerializer(Serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['name']

class BookSerializer(Serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        current_year = datetime.now().year 
        if value > current_year:
            raise serializers.ValidationError("The publication year cannot be in the future.")
            return value