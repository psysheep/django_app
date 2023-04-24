from library.models import Book

from django.db import models
from django.contrib.auth.models import User


class ReadingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    last_page_read = models.IntegerField()
    rating = models.IntegerField(default=None)
    started = models.DateTimeField(default=None)
    finished = models.DateTimeField(default=None)
