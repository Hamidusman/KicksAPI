from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'product', views.ProductViewSet, basename='product')
router.register(r'rating', views.RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]