from django.shortcuts import render
from rest_framework import status, permissions, generics, viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
  serializer_class = UserSerializer
  permission_classes = (permissions.AllowAny)


class ListUsrView(generics.ListAPIView):
  queryset = User.objects.all()
