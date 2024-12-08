from .models import User
from .serializers import SigninSerializer, UserSerializer, UserProfileSerialiser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


# 회원가입
class SignupView(APIView):
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


class SigninView(TokenObtainPairView):
    serializer_class = SigninSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerialiser(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerialiser(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
