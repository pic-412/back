from .models import User
from pic.places.models import Place
from .serializers import SigninSerializer, UserSerializer, UserProfileSerialiser, UserProfileUpdateSerialiser
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


# 회원가입
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
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                temp_likes = request.session.get('temp_likes', [-1])
                if temp_likes:
                    for place_id in temp_likes:
                        try:
                            place = Place.objects.get(id=place_id)
                            place.likes.add(user)
                        except ObjectDoesNotExist:
                            pass
                    request.session.pop('temp_likes', None)
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
        response = super().post(request, *args, **kwargs)
    
        if response.status_code == 200: 
            user = request.user
            temp_likes = request.session.get('temp_likes', [-1])
            if temp_likes:
                for place_id in temp_likes:
                    try:
                        place = Place.objects.get(id=place_id)
                        place.likes.add(user)
                    except ObjectDoesNotExist:
                        pass
                request.session.pop('temp_likes', None)
        return response


# 회원 프로필 조회, 수정, 탈퇴
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
        try:
            request.user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
