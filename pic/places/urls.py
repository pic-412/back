from django.urls import path
from .views import PlaceRandomView, PlaceDetailView, PlaceLikeView, MyPicView


urlpatterns = [
    path('places/random/', PlaceRandomView.as_view()),
    path('places/<int:place_id>/', PlaceDetailView.as_view()),
    path('places/<int:place_id>/likes', PlaceLikeView.as_view()),
    path('places/pic', MyPicView.as_view()),
]
