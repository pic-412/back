# from django.contrib import admin
# from django.urls import path, include

# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     # path('api/accounts/', include('pic.accounts.urls')),
# ]
from django.urls import path

from .views import ExampleView

urlpatterns = [
    path('', ExampleView.as_view(), name='examples'),
]
