from django.utils.timezone import now
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=80, blank=False)
    surname = models.CharField(max_length=80, blank=False)
    country = models.CharField(max_length=80, blank=False)
    birthday = models.DateField(default=now)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Genre(models.Model):
    genre = models.CharField(max_length=80, blank=False)

    def __str__(self):
        return f'{self.genre}'


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publishing_date = models.DateField()
    genres = models.ManyToManyField(Genre)
    description = models.TextField(default='')
    pdf = models.FileField(upload_to='library/static/books', default=None)

    def __str__(self):
        return f'{self.title}'

    def get_many_string(self):
        authors = ', '.join(str(author) for author in self.authors.all())
        genres = ', '.join(str(genre) for genre in self.genres.all())
        return {'authors': authors, 'genres': genres}
