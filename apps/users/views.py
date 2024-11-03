from django.shortcuts import render
from rest_framework.decorators import action
from .models import User, Profile
from rest_framework.viewsets import ModelViewSet
from .serializers import ProfileSerializer
from djoser.views import UserViewSet
from rest_framework.response import Response
# Create your views here.

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileSerializer(data=request.data)
        serializer.save(user=user)
        return Response(serializer.data, status=201)