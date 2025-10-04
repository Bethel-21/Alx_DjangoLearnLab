from django.db import models
from django.conf import settings
from django.urls import reverse

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