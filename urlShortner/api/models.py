from django.db import models


class URL(models.Model):
    original_url=models.URLField(max_length=200)
    short_url=models.CharField(max_length=6, unique=True, blank=True)
    expiration_date = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.original_url

