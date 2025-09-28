from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()  # Use IntegerField
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Use ForeignKey, not OneToOneField

    def __str__(self):
        return self.title
