from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts', include('pic.accounts')),
    path('places', include('pic.places')),
]
