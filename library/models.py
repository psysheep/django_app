from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
1

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


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, blank=True, null=True)
    subject = models.CharField(max_length=30, blank=True)
    text = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject} - {self.user.username}'

    class Meta:
        ordering = ['-created_at']
        unique_together = ('book', 'user',)


class ReadingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    started = models.DateField(default=now)
    finished = models.DateField(null=True)
    last_page = models.IntegerField(null=True, default=0)

    class Meta:
        unique_together = ('book', 'user',)
