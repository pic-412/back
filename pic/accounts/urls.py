from django.urls import path
from . import views


urlpatterns = [
    path("", views.SignupView.as_view()),
    path("signin", views.SigninView.as_view()),
]