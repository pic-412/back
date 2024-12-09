from .models import User
from .serializers import SigninSerializer, UserSerializer, UserProfileSerialiser
from drf_spectacular.utils import extend_schema
from .validators import validate_user_data
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


# 회원가입
class SignupView(APIView):
    @extend_schema(
        tags=['유저'],
        summary="회원가입",
        description="회원가입 API",
        request=UserSerializer,
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_201_CREATED: "str",
            status.HTTP_400_BAD_REQUEST: "에러!"
        }
    )
    def post(self, request):

        errors = validate_user_data(request.data)
        if errors is not None:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=request.data.get("email"),
            password=request.data.get("password"),
            nickname=request.data.get("nickname")
        )

        refresh = RefreshToken.for_user(user)
        response_dict = {"message": "회원 가입 완료"}
        response_dict['access'] = str(refresh.access_token)
        response_dict['refresh'] = str(refresh)
        return Response(response_dict)


class SigninView(TokenObtainPairView):
    serializer_class = SigninSerializer


# 회원 프로필 조회, 수정, 탈퇴
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['프로필'],
        summary="프로필 조회",
        description="프로필 조회 API",
        responses={
            status.HTTP_200_OK: UserProfileSerialiser,
            status.HTTP_400_BAD_REQUEST: "에러!"
        }
    )
    def get(self, request):
        serializer = UserProfileSerialiser(request.user)
        return Response(serializer.data)

    @extend_schema(
        tags=['회원정보 수정'],
        summary="회원정보 수정",
        description="닉네임, 비밀번호 변경 가능",
        request=UserSerializer,
        responses={
            status.HTTP_200_OK: UserProfileSerialiser,
            status.HTTP_201_CREATED: "str",
            status.HTTP_400_BAD_REQUEST: "닉네임을 10자 이하의 영문자와 숫자 조합으로 설정해 주세요.",
            status.HTTP_404_NOT_FOUND: "찾을 수 없음",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "서버 에러"
        }
    )
    def put(self, request):
        serializer = UserProfileSerialiser(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['회원탈퇴'],
        summary="회원탈퇴",
        description="현재 로그인한 사용자의 계정을 삭제합니다.",
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: "에러!",
            status.HTTP_401_UNAUTHORIZED: "인증되지 않은 사용자",
            status.HTTP_404_NOT_FOUND: "찾을 수 없음",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "서버 에러"
        }
    )
    def delete(self, request):
        try:
            request.user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
