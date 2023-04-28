from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('<slug:username>/', views.UserDetails.as_view(), name='user_page'),
]
