from django.urls import path
from . import views


urlpatterns = [
    path("", views.UserSignupView.as_view()),  # 회원가입
]