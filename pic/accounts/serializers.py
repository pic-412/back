from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re


class UserSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'password_check')
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        password_check = data.get("password_check")
        nickname = data.get("nickname")

        # email_patten = r''
        # if not re.match(email_patten, email):
        #     raise serializers.ValidationError({"error": "email 형식이 아닙니다. 확인해주세요."})

        if password != password_check:
            raise serializers.ValidationError({"error": "password가 일치하지 않습니다. 확인해주세요."})
        if len(password) < 8 or len(password) > 32:
            raise serializers.ValidationError({"error": "password는 8-32자리여야 합니다."})
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!#$%^&?])[\w!#$%^&?]{8,32}$', password):
            raise serializers.ValidationError({"error": "password는 영문, 숫자, 특수문자(!#$%^&?) 조합 8-32 자리여야 합니다."})

        return data
    
    def create(self, validated_data):
        password_check = validated_data.pop('password_check', None)
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'nickname')
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileUpdateSerialiser(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('nickname', 'password', 'password_check')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'nickname': {'required': False}
        }
    
    def validate(self, data):
        password = data.get("password")
        password_check = data.get("password_check")
        nickname = data.get("nickname")

        if password:
            if password != password_check:
                raise serializers.ValidationError({"error": "password가 일치하지 않습니다. 확인해주세요."})
            if len(password) < 8 or len(password) > 32:
                raise serializers.ValidationError({"error": "password는 8-32자리여야 합니다."})
            pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!#$%^&?])[\w!#$%^&?]{8,32}$'
            if not re.match(pattern, password):
                raise serializers.ValidationError({"error": "password는 영문, 숫자, 특수문자(!#$%^&?) 조합 8-32 자리여야 합니다."})

        if nickname:
            if User.objects.filter(nickname=nickname).exists():
                    raise serializers.ValidationError({"error": "이미 존재하는 nickname 입니다."})
            if not re.match(r'^[a-zA-Z0-9]{1,10}$', nickname):
                raise serializers.ValidationError({"error": "닉네임을 10자 이하의 영문자와 숫자 조합으로 설정해 주세요."})
        
        data.pop('password_check', None)

        return data


class SigninSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
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
