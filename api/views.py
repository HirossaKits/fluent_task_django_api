from django.db.models import query
from api.models import User, Profile, PersonalSettings, Project,Task, TaskCategory
from rest_framework import status, permissions, generics, viewsets
from rest_framework.response import Response
from .serializers import ProjectSerializer, TaskSerializer, UserSerializer, ProfileSerializer


class CreateUserView(generics.CreateAPIView):
  serializer_class = UserSerializer
  permission_classes = (permissions.AllowAny,)


class LoginUserView(generics.RetrieveAPIView):
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticated,)

  def get_object(self):
    return self.request.user


class UpdateUserView(generics.UpdateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticated,)


class ProfileViewSet(viewsets.ModelViewSet):
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def destroy(self, request, *args, **kwargs):
    response = {'message': 'DELETE is not allowed.'}
    return Response(response, status=status.HTTP_400_BAD_REQUEST)

  def partial_update(self, request, *args, **kwargs):
    response = {'message': 'PATCH is not allowed.'}
    return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PersonalSettingsViewSet(viewsets.ModelViewSet):
  queryset = PersonalSettings.objects.all()
  serializers_class = ProfileSerializer


class ProjectViewSet(viewsets.ModelViewSet):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer

  # def perform_create(self, serializer):
  #   serializer.save(resp_user=self.request.user, member=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

  # def perform_create(self, serializer):
  #   serializer.save(assigned=self.request.user, author=self.request.user)


# class TaskCategoryViewSet(viewsets.ModelViewSet):
#   queryset = TaskCategory.objects.all()
#   serializer_class = TaskCategory
from django.shortcuts import render

# Create your views here.
