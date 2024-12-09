import re
from .models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'nickname')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_nickname(self, value):
        if not re.match(r'^[a-zA-Z0-9]{1,10}$', value):
            raise serializers.ValidationError(
                "닉네임을 10자 이하의 영문자와 숫자 조합으로 설정해 주세요.")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class SigninSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["nickname"] = self.user.nickname
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
