from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken


# 회원가입
class UserSignupView(APIView):
    def post(self, request):
        user = User.objects.create_user(
            email=request.data.get("email"),
            password=request.data.get("password"),
            nickname=request.data.get("nickname")
        )

        refresh = RefreshToken.for_user(user)
        response_dict = {"message": "회원가입이 완료되었습니다."}
        response_dict['access'] = str(refresh.access_token)
        response_dict['refresh'] = str(refresh)
        return Response(response_dict)