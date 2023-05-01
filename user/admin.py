from django.contrib import admin
from .models import ReadingProgress, RatingReview


class RatingReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'review', 'rating', 'date')


admin.site.register(ReadingProgress)
admin.site.register(RatingReview, RatingReviewAdmin)
