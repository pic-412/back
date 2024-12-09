from .models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'password_check')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfileSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'nickname')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class SigninSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        # 사용자 이름 필드 확인 (일반적으로 'username' 또는 'email')
        email = attrs.get('email')
        password = attrs.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"errors": "가입한 회원이 아닙니다. email 확인 또는 회원가입을 진행해주세요."})

        if not user.check_password(password):
            raise serializers.ValidationError({"errors": "email, password 확인해주세요."})
        
        try:
            data = super().validate(attrs)
        except serializers.ValidationError:
            raise serializers.ValidationError({"errors": "email, password 확인해주세요."})

        refresh = self.get_token(self.user)

        data["nickname"] = self.user.nickname
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
