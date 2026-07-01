from django.db import models
from django.conf import settings
from apps.books.models import Book

class Shelf(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='shelves'
    )
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='shelves', blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"