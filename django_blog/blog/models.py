from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = 'posts'
    )


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        # returns the canonical URL for a post instance
        return reverse('post_detail', args=[str(self.id)])



class Comment(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments'
    )  # many comments -> one post

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )  # who wrote the comment

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']  # oldest first; change to '-created_at' for newest first

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'




class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# In your existing Post model add:
class Post(models.Model):
    # ... existing fields: title, content, author, published_date, etc.
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    # rest of Post (methods, Meta, etc.)