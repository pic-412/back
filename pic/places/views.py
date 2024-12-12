import random
from .serializers import PlaceSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
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
                description="더 이상 보여줄 장소가 없습니다."
            )

        }
    )
    def get(self, request):
        """
        랜덤 장소 사진 API
        """
        viewed_place_id = request.session.get('viewed_random_places', [])
        all_place = Place.objects.all()
        all_place_id = [place.id for place in all_place]
        # 아직 안 본 장소 찾기
        unviewed_place_id = []
        for place_id in all_place_id:
            # 아직 보지 않은 장소라면 추가
            if place_id not in viewed_place_id:
                unviewed_place_id.append(place_id)

        # 보지 않은 장소가 없으면 세션 초기화
        if not unviewed_place_id:
            viewed_place_id = []
            unviewed_place_id = list(all_place_id)  # 모든 장소 사진 다시 보여줌

        # 랜덤 장소 사진 선택
        random_place_id = random.choice(unviewed_place_id)
        place = get_object_or_404(Place, id=random_place_id)

        # 보여준 장소 id는 해당 세션에 추가
        viewed_place_id.append(random_place_id)
        request.session['viewed_random_places'] = viewed_place_id

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
            'time': place.time,
            'image_url': place.image_url,
            'naver_url': place.naver_url
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


class MyPicView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        tags=['MyPic'],
        summary="MyPic API",
        description="MyPic 장소 중 랜덤으로 1개 사진이 나옵니다.",
        responses={
            200: OpenApiResponse(
                description="MyPic 중 랜덤 사진을 성공적으로 조회함"
            ),
            400: OpenApiResponse(
                description="잘못된 요청"
            ),
            401: OpenApiResponse(
                description="로그인이 필요합니다"
            ),
            404: OpenApiResponse(
                description="더 이상 보여줄 장소가 없습니다."
            ),
            500: OpenApiResponse(
                description="서버 에러"
            )
        }
    )
    def get(self, request):
        """
        [ my pic page ]
        사용자가 좋아요한 장소 사진 랜덤으로 나타내기(중복 방지)
        """
        # 사용자의 좋아요 목록 가져옴
        my_likes = Like.objects.filter(account=request.user)
        # 장소들 id 리스트로
        liked_place_id = [like.place_id for like in my_likes]

        # 좋아요한 장소가 없을 때
        if not liked_place_id:
            return Response({
                'message': '좋아요한 장소가 없습니다.'
            }, status=status.HTTP_404_NOT_FOUND)

        # 세션에 이미 본 장소들 id 관리 (없으면 빈 리스트 반환)
        viewed_place_id = request.session.get('viewed_my_pic_places', [])

        # 아직 보지 않은 좋아요 장소들 필터링
        unviewed_place_id = []
        for place_id in liked_place_id:
            # 아직 보지 않은 장소라면 추가
            if place_id not in viewed_place_id:
                unviewed_place_id.append(place_id)

        # 아직 보지 않은 장소가 없으면 세션 초기화
        if not unviewed_place_id:
            viewed_place_id = []
            unviewed_place_id = list(liked_place_id)  # 좋아요한 모든 장소 사진 보여줌

        # 랜덤 장소 사진 선택
        random_place_id = random.choice(unviewed_place_id)
        place = get_object_or_404(Place, id=random_place_id)

        # 보여준 장소 id는 해당 세션에 추가
        viewed_place_id.append(random_place_id)
        request.session['viewed_my_pic_places'] = viewed_place_id

        place_info = {
            'id': place.id,
            'name': place.place,
            'address': place.adress,
            'time': place.time,
            'image_url': place.image_url,
            'naver_url': place.naver_url
        }
        return Response(place_info)