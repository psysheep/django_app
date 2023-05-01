from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("review/", views.ReviewList.as_view(), name="review_n"),
    path("review/<int:pk>/", views.LeaveRatingReview.as_view(), name="leave_review_n"),
    # path("review/<int:book_pk>/", views.leave_review, name="leave_review_n"),
]
