from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models

from library.models import Book


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
