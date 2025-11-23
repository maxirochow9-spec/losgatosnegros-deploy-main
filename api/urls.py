from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet

router = DefaultRouter()
router.register(r'products', ProductoViewSet, basename='producto')

urlpatterns = [
    path('', include(router.urls)),
]
