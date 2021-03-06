from django.db.models import query
from api.models import User, Profile, PersonalSetting, Project, Task, TaskCategory
from rest_framework import status, permissions, generics, viewsets, mixins
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer, PersonalSettingSerializer, ProjectSerializer, \
    CategorySerializer, TaskSerializer
from . import custompermissions


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class LoginUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = {'message': 'PUT method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, custompermissions.ProfilePermission)

    def get_queryset(self):
        users = User.objects.filter(org=self.request.user.org).select_related('org')
        return self.queryset.filter(user__in=users)

    def perform_create(self, serializer):
        response = {'message': 'POST is not allowed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'DELETE is not allowed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH is not allowed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# Allow only PUT
class PersonalSettingViewSet(viewsets.ModelViewSet):
    queryset = PersonalSetting.objects.all()
    serializer_class = PersonalSettingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        response = {'message': 'POST is not allowed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH is not allowed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# Allow GET, POST, PUT, DELETE
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return self.queryset.filter(member=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH is not allowed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# Allow GET, POST, PUT, DELETE
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = TaskCategory.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        projects = Project.objects.filter(member=self.request.user).prefetch_related('member').values_list("id")
        return self.queryset.filter(project__in=projects)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH is not allowed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        projects = Project.objects.filter(member=self.request.user).prefetch_related('member').values_list("id")
        return self.queryset.filter(project__in=projects)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# class TaskCategoryViewSet(viewsets.ModelViewSet):
#   queryset = TaskCategory.objects.all()
#   serializer_class = TaskCategory
from django.shortcuts import render

# Create your views here.
