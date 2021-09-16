from api.models import Profile, Project, TaskCategory, Task, PersonalSettings
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
    fields = ['avatar_img','desctiption']
    # extra_kwargs = {'user': {'read_only': True}}

class PersonalSettingsSerializer(serializers.ModelSerializer):
  class Meta:
    model = PersonalSettings
    fields = ['dark_mode','view_only_owned','selected_project']


class CategorySerializer(serializers.ModelSerializer):
  project_id = serializers.CharField(read_only=True)
  category_id = serializers.CharField(source='id', read_only=True)
  category_name = serializers.CharField(source='name')

  class Meta:
    model = TaskCategory
    fields = ['project_id',
              'category_id',
              'category_name']

  def create(self, validated_data):
    return TaskCategory.objects.create(**validated_data)


class TaskSerializer(serializers.ModelSerializer):
  task_id = serializers.CharField(source='id', read_only=True)
  task_name = serializers.CharField(source='name')
  project_id = serializers.CharField()
  category_id = serializers.CharField(source='category')

  class Meta:
    model = Task
    fields = ['project_id',
              'task_id',
              'task_name',
              'category_id',
              'status',
              'description',
              'estimate_manhour',
              'actual_manhour',
              'scheduled_startdate',
              'scheduled_enddate',
              'actual_startdate',
              'actual_enddate',
              'created_at',
              'update_at']


class PorjectCategorySerializer(serializers.ModelSerializer):
  category_id = serializers.CharField(source='id', read_only=True)
  category_name = serializers.CharField(source='name')

  class Meta:
    model = TaskCategory
    fields = ['category_id',
              'category_name']


class PorjectTaskSerializer(serializers.ModelSerializer):
  task_id = serializers.CharField(source='id', read_only=True)
  task_name = serializers.CharField(source='name')
  category_id = serializers.CharField(source='category')

  class Meta:
    model = Task
    fields = ['project_id',
              'task_id',
              'task_name',
              'category_id',
              'status',
              'description',
              'estimate_manhour',
              'actual_manhour',
              'scheduled_startdate',
              'scheduled_enddate',
              'actual_startdate',
              'actual_enddate',
              'created_at',
              'update_at']


class ProjectSerializer(serializers.ModelSerializer):
  category = PorjectCategorySerializer(source='project_category', many=True, read_only=True)
  task = PorjectTaskSerializer(source='project_task', many=True, read_only=True)
  project_id = serializers.CharField(source='id', read_only=True)
  project_name = serializers.CharField(source='name')

  class Meta:
    model = Project
    fields = ['project_id',
              'project_name',
              'resp_user',
              'member',
              'description',
              'category',
              'task']