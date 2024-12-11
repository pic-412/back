import random
from .serializers import PlaceSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Place, Like


class PlaceRandomView(APIView):
    @extend_schema(
        tags=['장소'],
        summary="랜덤 장소 사진",
        description="랜덤으로 하나의 장소의 사진이 나옵니다.",
        responses={
            200: OpenApiResponse(
                description="랜덤 장소 사진을 성공적으로 조회함"
            ),
            400: OpenApiResponse(
                description="잘못된 요청"
            ),
            404: OpenApiResponse(
                description="장소를 찾을 수 없음"
            )

        }
    )
    def get(self, request):
        """
        랜덤 장소 사진 API
        """
        random_place_id = random.randint(1, 3)      # id값을 랜덤으로 돌려 랜덤 사진
        place = get_object_or_404(Place, id=random_place_id)

        place_info = {
            'id': place.id,
            'image_url': place.image_url
        }
        return Response(place_info)


class PlaceDetailView(APIView):
    @extend_schema(
        tags=['장소'],
        summary="장소 상세 정보",
        description="장소 상세 정보를 반환합니다.",
        responses={
            200: OpenApiResponse(
                description="장소 상세 정보를 성공적으로 조회함"
            ),
            400: OpenApiResponse(
                description="잘못된 요청"
            ),
            404: OpenApiResponse(
                description="장소를 찾을 수 없음"
            )
        }
    )
    def get(self, request, place_id):
        """
        장소 상세 API
        """
        place = get_object_or_404(Place, id=place_id)

        place_info = {
            'id': place.id,
            'name': place.place,
            'address': place.adress,
            'time': place.time
        }

        return Response(place_info)


class PlaceLikeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['좋아요'],
        summary="장소 좋아요",
        description="장소를 좋아요 합니다.",
        responses={
            200: OpenApiResponse(
                response=PlaceSerializer,
                description="좋아요 추가 성공"
            ),
            400: OpenApiResponse(
                description="이미 좋아요한 장소입니다"
            ),
            401: OpenApiResponse(
                description="로그인이 필요합니다"
            ),
            404: OpenApiResponse(
                description="장소를 찾을 수 없음"
            ),
            500: OpenApiResponse(
                description="서버 에러"
            )
        }
    )
    def post(self, request, place_id):
        """
        장소 좋아요 API
        """
        place = get_object_or_404(Place, id=place_id)
        # 좋아요 반영
        Like.objects.create(account=request.user, place=place)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        tags=['좋아요'],
        summary="장소 좋아요 취소",
        description="좋아요한 장소를 취소합니다.",
        responses={
            204: OpenApiResponse(
                description="좋아요 취소 성공"
            ),
            400: OpenApiResponse(
                description="좋아요하지 않은 장소입니다"
            ),
            401: OpenApiResponse(
                description="로그인이 필요합니다"
            ),
            404: OpenApiResponse(
                description="장소를 찾을 수 없음"
            ),
            500: OpenApiResponse(
                description="서버 에러"
            )
        }
    )
    def delete(self, request, place_id):
        """
        장소 좋아요 취소 API
        """
        place = get_object_or_404(Place, id=place_id)
        # 좋아요 취소
        Like.objects.filter(account=request.user, place=place).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
