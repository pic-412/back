from .models import User
from django.core.validators  import validate_email
from django.core.exceptions  import ValidationError
import re

def validate_user_data(user_data):
    email = user_data.get("email")
    password = user_data.get("password")
    password_check = user_data.get("password_check")
    nickname = user_data.get("nickname")

    # email 형식 검증 
    try:
        validate_email(email)
    except ValidationError:
        return "email 형식이 아닙니다. 확인해주세요."
    
    # email 중복 여부 확인
    if User.objects.filter(email=email).exists():
        return "이미 존재하는 email 입니다."
    
    if password != password_check:
        return "password 일치하지 않습니다. 확인해주세요."
    
    # password 최소 길이 검증
    if len(password) < 8:
        return "password 8자리 이상 입력해주세요. 영문, 숫자, 특수문자(!#$%^&?) 조합 8-32 자리입니다."
    
    if len(password) >= 32:
        return "password 32자리 이하 입력해주세요. 영문, 숫자, 특수문자(!#$%^&?) 조합 8-32 자리입니다."
    
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!#$%^&?]).{8,32}$'
    if not re.match(pattern, password):
        return "password 영문, 숫자, 특수문자(!#$%^&?) 조합 8-32 자리입니다."

    if User.objects.filter(nickname=nickname).exists():
        return "이미 존재하는 nickname 입니다."