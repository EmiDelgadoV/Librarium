from django.db import models
from django.conf import settings

class Book(models.Model):
    STATUS_CHOICES = [
        ('quiero_leer', 'Quiero leer'),
        ('leyendo', 'Leyendo'),
        ('leido', 'Leído'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='books'
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='quiero_leer'
    )
    cover_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.author}"