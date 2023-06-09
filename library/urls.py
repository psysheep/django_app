from django.urls import path
from . import views

app_name = "library"
urlpatterns = [
    path('books/', views.BookList.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetail.as_view(), name='book'),
    path('book/<int:book_pk>/page/<int:page_number>/', views.page_view, name='page_view'),
]
