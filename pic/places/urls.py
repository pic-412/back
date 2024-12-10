from django.urls import path
from .views import RandomPlaceView
from . import views

urlpatterns = [
    path('places/random/', RandomPlaceView.as_view()),
    path('places/<int:place_id>/', views.PlaceDetailView.as_view()),
]
