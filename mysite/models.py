# tutaj tdodaj model zdjecia, z polami description, created( data), relacje do klasy /tabeli User
# musisz odpalic makemigrations, migrate
from django.contrib.auth.models import User
from django.db import models

class Photo(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.TextField()
    created = models.DateTimeField()


class Observation(models.Model):
    follower = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_observation')
        ]


class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField()
