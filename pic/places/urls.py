from django.urls import path
from .views import PlaceRandomView, PlaceDetailView, PlaceLikeView


urlpatterns = [
    path('places/random/', PlaceRandomView.as_view()),
    path('places/<int:place_id>/', PlaceDetailView.as_view()),
    path('places/<int:place_id>/likes', PlaceLikeView.as_view()),
]
