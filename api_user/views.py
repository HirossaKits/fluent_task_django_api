from django.db.models import query
from core.models import Profile, Project, Task, TaskCategory
from rest_framework import status, permissions, generics, viewsets
from rest_framework.response import Response
from .serializers import ProjectSerializer, TaskSerializer, UserSerializer, ProfileSerializer
from api_user import serializers


class CreateUserView(generics.CreateAPIView):
  serializer_class = UserSerializer
  permission_classes = (permissions.AllowAny,)


class LoginUserView(generics.RetrieveAPIView):
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user


class UpdateUserView(generics.UpdateAPIView):
  serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
  queryset = Profile.object.all()
  serializer_class = ProfileSerializer

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def destroy(self, request, *args, **kwargs):
    response = {'message': 'DELETE is not allowed.'}
    return Response(response, status=status.HTTP_400_BAD_REQUEST)

  def partial_update(self, request, *args, **kwargs):
    response = {'message': 'PATCH is not allowed.'}
    return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(viewsets.ModelViewSet):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer

  def perform_create(self, serializer):
    serializer.save(resp_user=self.request.user, member=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

  def perform_create(self, serializer):
    serializer.save(assigned=self.request.user, author=self.request.user)


class TaskCategoryViewSet(viewsets.ModelViewSet):
  queryset = TaskCategory.objects.all()
  serializer_class = TaskCategory
