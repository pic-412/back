from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/accounts/kakao', include('allauth.urls')),
    path('api/accounts/', include('pic.accounts.urls')),
    path('api/places/', include('pic.places.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 