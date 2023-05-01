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


class RatingReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=200, blank=True)
    rating = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.book.title} {self.review}"
