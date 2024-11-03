from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'profile', views.ProfileViewSet, basename='usersss')

urlpatterns = router.urls