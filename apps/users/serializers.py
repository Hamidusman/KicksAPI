from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import User, Profile

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
                'firstname', 'lastname',
                'state', 'region',
                'address', 'phone_number',
                'avatar', 'user', 'created_at'
                ]
        
        read_only_field = ['user', 'created_at']
        