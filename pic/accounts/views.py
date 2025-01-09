from .serializers import SigninSerializer, UserSerializer, UserProfileSerialiser, UserProfileUpdateSerialiser
from .models import User
from config.settings import base
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login, authenticate
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import bcrypt


class SignupView(APIView):
    @extend_schema(
        tags=['회원'],
        summary="회원가입",
        description="회원가입 API, 비회원이 회원가입을 진행합니다.",
        request=UserSerializer,
        responses={
            201: OpenApiResponse(
                description="회원 가입 완료, 유저 생성"
            ),
            400: OpenApiResponse(
                description="email, password 입력값이 잘못된 경우"
            ),
        }
    )
    def post(self, request):
        """
        회원가입 API
        """
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_dict = {
            "message": "회원 가입 완료",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
            }
            return Response(response_dict, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(TokenObtainPairView):

    serializer_class = SigninSerializer

    @extend_schema(
        tags=['회원'],
        summary="로그인",
        description="로그인 API, 가입 회원이 email,password 입력해 로그인합니다.",
        responses={
            200: OpenApiResponse(
                description="로그인, 해당 유저 nickname과 Token 발행 "
            ),
            400: OpenApiResponse(
                description="email, password 입력값이 잘못된 경우"
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        """
        로그인 API
        """
        return super().post(request, *args, **kwargs)


class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['회원'],
        summary="프로필 조회",
        description="프로필 조회 API, 로그인한 회원 프로필을 조회합니다.",
        responses={
            200: OpenApiResponse(
                description="프로필 조회, 해당 유저 email과 nickname 조회"
            ),
            400: OpenApiResponse(
                description="잘못된 요청"
            ),
            404: OpenApiResponse(
                description="프로필 조회 유저를 찾을 수 없는 경우"
            ),
            500: OpenApiResponse(
                description="서버 에러"
            )
        }
    )
    def get(self, request):
        """
        프로필 조회 API
        """
        serializer = UserProfileSerialiser(request.user)
        return Response(serializer.data)

    @extend_schema(
        tags=['회원'],
        summary="프로필 회원정보 수정",
        description="프로필 회원정보 수정 API, 유저 nickname과 password 정보를 수정합니니다.",
        request=UserProfileUpdateSerialiser,
        responses={
            200: OpenApiResponse(
                description="회원정보 수정 완료, 해당 유저 email과 nickname 조회"
            ),
            400: OpenApiResponse(
                description="수정하려는 nickname, password 입력값이 잘못된 경우"
            ),
            401: OpenApiResponse(
                description="로그아웃 상태로 요청하는 경우"
            ),
            500: OpenApiResponse(
                description="서버 에러"
            )
        }
    )
    def put(self, request):
        """
        프로필 수정 API
        """
        serializer = UserProfileUpdateSerialiser(request.user, data=request.data, partial=True)
        user = request.user
        if serializer.is_valid():
            password = request.data.pop('password', None)
            serializer.save()
            user.set_password(password)
            user.save()
            return Response({"message": "회원정보 수정 완료"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['회원'],
        summary="회원탈퇴",
        description="회원탈퇴 API, 유저정보를 DB에서 완전 삭제합니다.",
        responses={
            204: OpenApiResponse(
                description="회원탈퇴 완료"
            ),
            400: OpenApiResponse(
                description="회원탈퇴 요청이 제대로 되지 않은 경우"
            ),
            401: OpenApiResponse(
                description="로그아웃 상태로 요청하는 경우"
            ),
            404: OpenApiResponse(
                description="해당 유저정보를 찾지 못한 경우"
            ),
            500: OpenApiResponse(
                description="서버 에러"
            )
        }
    )
    def delete(self, request):
        """
        회원탈퇴 API
        """
        try:
            request.user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class KakaoView:
    @extend_schema(
        tags=['카카오로그인'],
        summary="카카오로그인",
        description="카카오로그인 API",
        responses={
            200: OpenApiResponse(
                description="카카오로그인 완료"
            ),
            400: OpenApiResponse(
                description="카카오 이메일이 없는 경우와 같이 잘못된 요청청"
            ),
            500: OpenApiResponse(
                description="서버 에러"
            )
        }
    )
    def get(request):
        url = "https://kauth.kakao.com/oauth/token"

        # 요청 파라미터
        data = {
            "grant_type": "authorization_code",
            "client_id": base.KAKAO_REST_API_KEY,  # 카카오 REST API 키
            "redirect_uri": "http://127.0.0.1:8000/accounts/kakao/login/callback",  # 등록된 리다이렉트 URI
            "code": request.GET.get("code"),  # 인가 코드
        }

        # 요청 헤더
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }

        response = requests.get(url, params=data, headers=headers)
        token = response.json()
        check_error = token.get("error")
        if check_error:
            return redirect("accounts:sociallogin")
        
        access_token = token.get("access_token")
        kakao_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
        kakao_data = kakao_request.json()
        
        kakao_account = kakao_data.get("kakao_account")
        if not kakao_account or not kakao_account.get("email"):
            return Response({"error": "등록하려면 이메일이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        email = kakao_account.get("email")
        username = "kakao_"+email.split('@')[0]
        kakao_profile = kakao_account.get("properties")
        # nickname = kakao_profile.get("nickname")
        id = str(kakao_data.get("id"))
        id = id.encode('utf-8')
        password = bcrypt.hashpw(id, bcrypt.gensalt() ) 

        user, created = User.objects.get_or_create(username=username, defaults={
            'email':email,
        })

        if created:
            user.set_password(password)

        user.save()
        user =  authenticate(username=username, password=password)
        if user:
            # 인증된 사용자의 backend 명시
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user)
        
        return redirect("index")