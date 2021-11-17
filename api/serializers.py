from datetime import datetime
from api.models import Profile, Project, TaskCategory, Task, PersonalSetting
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id',
                  'email',
                  'org',
                  'password',
                  'is_active',
                  'is_premium',
                  'is_administrator']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        # ユーザーを作成
        user = get_user_model().objects.create_user(**validated_data)
        # Token.objects.create(user=user)

        # Profile を作成
        first_name = self.context['request'].data['first_name']
        last_name = self.context['request'].data['last_name']
        prof = Profile.objects.create(user=user, first_name=first_name, last_name=last_name, avatar_img='null.png',
                                      comment='')
        prof.save()

        # PersonalSettings を作成
        settings = PersonalSetting.objects.create(user=user, dark_mode=False, project=None)
        settings.save()

        # PrivateProject を作成
        project = Project.objects.create(name='個人プロジェクト', org=None, resp=user, member=user, description='',
                                         startdate=datetime.date.today(),
                                         enddate=datetime.date.today().timedelta(years=1))

        return user


# Organization


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects, source='user')

    class Meta:
        model = Profile
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'avatar_img',
            'comment']

        # extra_kwargs = {'user': {'read_only': True}}

    # def get_org(self, instance):
    #     user = get_user_model().objects.filter(id=instance.user.id)
    #     print(user)
    #     return user.value('org')


class PersonalSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalSetting
        fields = ['dark_mode',
                  'show_own',
                  'project_id', ]


class ProjectSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField(source='id', read_only=True)
    project_name = serializers.CharField(source='name')
    org_id = serializers.CharField()
    resp_id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects, many=True, source='resp')
    member_id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects, many=True, source='member')

    class Meta:
        model = Project
        fields = ['project_id',
                  'project_name',
                  'org_id',
                  'resp_id',
                  'member_id',
                  'description']

    def create(self, validated_data):

        member = validated_data.pop('member')
        project = Project.objects.create(**validated_data)
        for user in member:
            project.member.add(user)

            for item in ['設計', '製造', 'テスト']:
                category = TaskCategory.objects.create(project_id=project.id, name=item)
                category.save()

            return project


class CategorySerializer(serializers.ModelSerializer):
    project_id = serializers.CharField()
    project_name = serializers.SerializerMethodField()
    category_id = serializers.CharField(source='id', read_only=True)
    category_name = serializers.CharField(source='name')

    class Meta:
        model = TaskCategory
        fields = ['project_id',
                  'project_name',
                  'category_id',
                  'category_name']

    def create(self, validated_data):
        return TaskCategory.objects.create(**validated_data)

    def get_project_name(self, instance):
        return instance.project.name


class TaskSerializer(serializers.ModelSerializer):
    task_id = serializers.CharField(source='id', read_only=True)
    task_name = serializers.CharField(source='name')
    project_id = serializers.CharField()
    project_name = serializers.SerializerMethodField(read_only=True)
    category_id = serializers.CharField()
    category_name = serializers.SerializerMethodField()
    assigned_id = serializers.CharField()
    assigned_name = serializers.SerializerMethodField(read_only=True)
    author_id = serializers.CharField()
    author_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = ['task_id',
                  'task_name',
                  'project_id',
                  'project_name',
                  'category_id',
                  'category_name',
                  'assigned_id',
                  'assigned_name',
                  'author_id',
                  'author_name',
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
        extra_kwargs = {'author_id': {'read_only': True}}

    def get_project_name(self, instance):
        return instance.project.name

    def get_category_name(self, instance):
        return instance.category.name if instance.category is not None else ''

    def get_author_name(self, instance):
        return f'{instance.author.last_name} {instance.author.first_name}' if instance.author is not None else ''

    def get_assigned_name(self, instance):
        return f'{instance.assigned.last_name} {instance.assigned.first_name}' if instance.assigned is not None else ''
    # def create(self, validated_data):
    #     print(validated_data)
    #     return Task.objects.create(**validated_data)

# class PorjectCategorySerializer(serializers.ModelSerializer):
#   category_id = serializers.CharField(source='id', read_only=True)
#   category_name = serializers.CharField(source='name')
#
#   class Meta:
#     model = TaskCategory
#     fields = ['category_id',
#               'category_name']
#
#
# class PorjectTaskSerializer(serializers.ModelSerializer):
#   task_id = serializers.CharField(source='id', read_only=True)
#   task_name = serializers.CharField(source='name')
#   category_id = serializers.CharField(source='category')
#
#   class Meta:
#     model = Task
#     fields = ['project_id',
#               'task_id',
#               'task_name',
#               'category_id',
#               'status',
#               'description',
#               'estimate_manhour',
#               'actual_manhour',
#               'scheduled_startdate',
#               'scheduled_enddate',
#               'actual_startdate',
#               'actual_enddate',
#               'created_at',
#               'update_at']
#
#
# class ProjectSerializer(serializers.ModelSerializer):
#   category = PorjectCategorySerializer(source='project_category', many=True, read_only=True)
#   task = PorjectTaskSerializer(source='project_task', many=True, read_only=True)
#   project_id = serializers.CharField(source='id', read_only=True)
#   project_name = serializers.CharField(source='name')
#
#   class Meta:
#     model = Project
#     fields = ['project_id',
#               'project_name',
#               'resp_user',
#               'member',
#               'description',
#               'category',
#               'task']
