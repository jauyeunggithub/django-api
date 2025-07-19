# urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimalViewSet, UserViewSet

# Register the viewsets with the router
router = DefaultRouter()
router.register(r'animals', AnimalViewSet, basename='animal')
router.register(r'users', UserViewSet)

# Manually specify an additional URL pattern to test explicit routes
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
