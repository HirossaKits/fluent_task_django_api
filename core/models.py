from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator
import uuid
from django.utils import timezone

# アバター画僧のアップロードパス


def upload_avatar_path(instance, filename):
  ext = filename.split('.')[-1]
  return '/'.join(['avatars', str(instance.user_profile.id) + str(".") + str(ext)])

# カスタムユーザーマネージャー


class UserManager(BaseUserManager):

  # ユーザー作成時
  def create_user(self, email, password=None, **extra_fields):

    if not email:
      raise ValueError('Email required.')

    # emailの正規化
    user = self.model(email=self.normalize_email(email), **extra_fields)
    # パスワードのハッシュ化
    user.set_password(password)
    # ユーザーをデータベースに保存
    user.save(using=self._db)

    return user

  # スーパーユーザー作成時
  def create_superuser(self, email, password):
    user = self.create_user(email, password)
    user.is_staff = True
    user.is_superuser = True
    # ユーザーをデータベースに保尊
    user.save(using=self._db)

    return user

# カスタムユーザー


class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(max_length=50, unique=True)
  # ユーザーがアクティブかどうか
  is_active = models.BooleanField(default=True)
  # 管理サイトへのアクセス許可
  is_staff = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  objects = UserManager()

  # emailをユーザー名として使用
  USERNAME_FIELD = 'email'

  def __str__(self):
    return self.email


class Profile(models.Model):
  user = models.OneToOneField(
      settings.AUTH_USER_MODEL,
      related_name='user',
      on_delete=models.CASCADE
  )
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)

  avatar_img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

  def __str__(self):
    return self.user.email


class Project(models.Model):
  id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
  resp_user = models.IntegerField(null=False, blank=False)
  name = models.CharField(blank=False, max_length=50)
  description = models.CharField(null=True, blank=True, max_length=250)
  start_date = models.DateTimeField(null=True)
  end_date = models.DateTimeField(null=True)

  def __str__(self):
    return self.name


class UserProjectRelation(models.model):
  user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      related_name='user',
      on_delete=models.CASCADE
  )
  project = models.ForeignKey(
      Project,
      related_name='project',
      on_delete=models.CASCADE
  )

  def __str__(self):
    return f'{self.project.name}_{self.user.first_name} {self.user.last_name}'


class Task(models.Model):
  STATUS = (
      ('0', 'Not started'),
      ('1', 'On going'),
      ('2', 'Done')
  )
  id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
  project = models.ForeignKey(
      Project,
      related_name='user_project',
      on_delete=models.CASCADE
  )
  assigned = models.IntegerField(null=False, blank=False)
  author = models.IntegerField(null=False, blank=False)
  name = models.CharField(null=False, blank=False, max_length=50)
  category = models.IntegerField(null=False, blank=False)
  description = models.CharField(max_length=250)
  status = models.CharField(max_length=20, choices=STATUS, default='0')
  estimate_manhour = models.IntegerField(null=True, validators=[MinValueValidator(0)])
  actual_manhour = models.IntegerField(null=True, validators=[MinValueValidator(0)])
  start_date = models.DateField(null=True)
  end_date = models.DateField(null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name


class TaskCategory(models.Model):
  project = models.ForeignKey(
      Project,
      related_name='project',
      on_delete=models.CASCADE
  )
  name = models.CharField(null=False, blank=False)


class AlterResponsible(models.Model):
  project = models.ForeignKey(
      Project,
      related_name='project',
      on_delete=models.CASCADE
  )
  alter_from = models.IntegerField(null=False, blank=False)
  alter_to = models.IntegerField(null=False, blank=False)
