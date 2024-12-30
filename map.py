import requests
from config.settings.base import *

def get_coordinates(address, client_id, client_secret):
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }
    params = {"query": address}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['addresses']:
            latitude = float(data['addresses'][0]['y'])
            longitude = float(data['addresses'][0]['x'])
            return latitude, longitude
    return None

# 사용 예시
client_id = env("NEVER_MAP_API_KEY_ID")
client_secret = env("NEVER_MAP_API_KEY")
address = '제주특별자치도 제주시 협재리 2454'
coordinates = get_coordinates(address, client_id, client_secret)

if coordinates:
    print(f"위도: {coordinates[0]}, 경도: {coordinates[1]}")
else:
    print("좌표를 찾을 수 없습니다.")