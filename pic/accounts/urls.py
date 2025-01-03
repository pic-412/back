from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("", views.SignupView.as_view()),
    path("signin", views.SigninView.as_view()),
    path("profile", views.UserProfileView.as_view()),
    path("token_refresh", TokenRefreshView.as_view()),
    path("kakao/login/", views.KakaoLoginView.as_view(), name="kakao_login"),
    path("kakao/callback/", views.KakaoLoginView.as_view(), name="kakao_callback"),
]

