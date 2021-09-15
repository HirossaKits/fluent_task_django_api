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


class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Project
    fields = ['id',
              'resp_user',
              'member',
              'name',
              'description']


class CategorySerializer(serializers.ModelSerializer):
  # category_id = serializers.CharField(source='id', read_only=True)
  # project_id = serializers.CharField(source='project')
  # category_name = serializers.CharField(source='name')

  class Meta:
    model = TaskCategory
    # fields = ['category_id',
    #           'project_id',
    #           'category_name']
    fields = ['project',
              'name']

  def create(self, validated_data):
    print(validated_data)
    # validated_data['project_id'] = validated_data.get('project', None)
    # del validated_data['project']
    # validated_data['api_name'] = validated_data.get('name', None)
    # del validated_data['name']
    # print(validated_data)
    return TaskCategory.objects.create(**validated_data)


class TaskSerializer(serializers.ModelSerializer):
  task_id = serializers.CharField(source='id')
  project_id = serializers.CharField()
  category_id = serializers.CharField(source='category')

  class Meta:
    model = Task
    fields = ['task_id',
              'project_id',
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

    read_only_fields = ['task_id',
              'project_id',
              'category_id',]