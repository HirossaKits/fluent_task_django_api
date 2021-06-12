from django.shortcuts import render

from rest_framework import generics
from api_user import serializers

class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer