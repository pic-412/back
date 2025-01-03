from .serializers import SigninSerializer, UserSerializer, KakaoSerializer, UserProfileSerialiser, UserProfileUpdateSerialiser
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import requests
import secrets


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



User = get_user_model()

class KakaoLoginView(APIView):
    serializer_class = KakaoSerializer

    @extend_schema(
        tags=['회원'],
        summary="카카오 로그인",
        description="카카오 OAuth를 통한 로그인/회원가입 API",
        responses={
            200: OpenApiResponse(description="로그인 성공, 토큰 발급"),
            400: OpenApiResponse(description="잘못된 요청 또는 카카오 인증 실패"),
            500: OpenApiResponse(description="서버 에러")
        }
    )
    def get(self, request):
        try:
            code = request.GET.get("code")
            if not code:
                return Response(
                    {"error": "인증 코드가 제공되지 않았습니다"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 카카오 토큰 받기
            token_response = requests.post(
                "https://kauth.kakao.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.KAKAO_REST_API_KEY,
                    "redirect_uri": settings.KAKAO_CALLBACK_URI,
                    "code": code,
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
                timeout=10
            )
            token_json = token_response.json()

            if "error" in token_json:
                return Response(
                    {"error": "카카오 토큰 발급 실패"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 유저 정보 받기
            user_info_response = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {token_json['access_token']}"},
                timeout=10
            )
            user_info = user_info_response.json()

            kakao_account = user_info.get("kakao_account")
            if not kakao_account or not kakao_account.get("email"):
                return Response(
                    {"error": "이메일 정보 제공에 동의해주세요"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            email = kakao_account["email"]
            username = f"kakao_{email.split('@')[0]}"
            # nickname = user_info.get(
            #     "properties", {}).get("nickname", username)

            # 안전한 랜덤 비밀번호 생성
            random_password = secrets.token_urlsafe(32)

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    # 'first_name': nickname,
                    'password': make_password(random_password)
                }
            )
            serializer = self.serializer_class(user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data, 
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'is_new_user': created
            }, status=status.HTTP_200_OK)

        except requests.Timeout:
            return Response(
                {"error": "카카오 서버 응답 시간 초과"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": f"로그인 처리 중 오류가 발생했습니다: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        serializer = UserProfileUpdateSerialiser(
            request.user, data=request.data, partial=True)
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
