# tutaj tdodaj model zdjecia, z polami description, created( data), relacje do klasy /tabeli User
# musisz odpalic makemigrations, migrate
from django.contrib.auth.models import User
from django.db import models

class Photo(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.TextField()
    created = models.DateTimeField()

