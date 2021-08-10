from core.models import Profile, Project, Task, PersonalSettings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ['id', 'email', 'password', 'first_name', 'last_name']
    extra_kwargs = {'password': {'write_only': True, 'required': True}}

  def create(self, validated_data):
    user = get_user_model().objects.create_user(**validated_data)
    Token.objects.create(user=user)
    return user


class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['id', 'user', 'avatar_img']
    extra_kwargs = {'user': {'read_only': True}}

class PersonalSettingsSerializer(serializers.ModelSerializer):
  class Meta:
    model = PersonalSettings
    fields = ['dark_mode','view_only_owned','selected_project']


class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Project
    fields = ['id', 'resp_user', 'member', 'name', 'description', 'start_date', 'end_date']


class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = ['id', 'project', 'assigned', 'author', 'name', 'description', 'status',
              'estimate_manhour', 'actual_manhour', 'start_date', 'end_date', 'created_at', 'update_at']
