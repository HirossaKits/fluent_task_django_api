from core.models import Profile, Project, Task
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'password']
    extra_kwargs = {'password': {'required': True}}

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    Token.objects.create(user=user)
    return user


class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['id', 'user', 'first_name', 'last_name', 'avatar_img']
    extra_kwargs = {'user': {'read_only': True}}


class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Project
    fields = ['id', 'resp_user', 'member', 'name', 'description', 'start_date', 'end_date']


class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = ['id', 'project', 'assigned', 'author', 'name', 'description', 'status',
              'estimate_manhour', 'actual_manhour', 'start_date', 'end_date', 'created_at', 'update_at']
