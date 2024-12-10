import random
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Place, Like


class RandomPlaceView(APIView):
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
            'latitude': float(place.latitude),    # float로 변환해서 반환
            'longitude': float(place.longitude),  # float로 변환해서 반환
            'image_url': place.image_url
        }

        return Response(place_info)


class PlaceLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, place_id):
        """
        장소 좋아요 API
        """
        place = get_object_or_404(Place, id=place_id)

        like.is_like = True
        like.save()
        post.like_count += 1
        post.save(update_fields=['like_count'])


class NewsFavorite(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, news_id):
        article = get_object_or_404(Article, id=news_id)
        # 해당 글 작성자는 글 즐겨찾기 못함
        if article.author == request.user:
            return Response("본인이 작성한 글은 즐겨찾기를 할 수 없습니다.", status=403)

        if request.user in article.favorite.all():
            article.favorite.remove(request.user)
            return Response("즐겨찾기 취소")
        else:
            article.favorite.add(request.user)
            return Response("즐겨찾기 완료!")


# 좋아요 취소 api
