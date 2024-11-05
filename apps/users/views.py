from django.shortcuts import render
from rest_framework.decorators import action
from .models import User, Profile
from rest_framework.viewsets import ModelViewSet
from .serializers import ProfileSerializer
from djoser.views import viewsets
from rest_framework.response import Response
from djoser.serializers import UserSerializer
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=["get"])
    def all_users(self, request):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileSerializer(data=request.data)
        serializer.save(user=user)
        return Response(serializer.data, status=201)