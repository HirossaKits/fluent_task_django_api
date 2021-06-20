from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status, permissions, generics, viewsets
from rest_framework.response import Response
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
  serializer_class = UserSerializer
  permission_classes = (permissions.AllowAny,)


class LoginUserView(generics.RetrieveUpdateAPIView):
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user


class UpdateUserView(generics.UpdateAPIView):
  serializer_class = UserSerializer
