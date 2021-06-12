from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.utils import timezone

# アバター画僧のアップロードパス
def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars',str(instance.user_profile.id)+ str(".")+ str(ext)])

# カスタムユーザーマネージャー
class UserManager(BaseUserManager):

    # ユーザー作成時
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Email required ')

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
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    # ユーザーがアクティブかどうか
    is_active = models.BooleanField(default=True)
    # 管理サイトへのアクセス許可
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.datetime.now)

    objects = UserManager()

    # emailをユーザー名として使用
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Profile(models.Model):
    user_email = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='user_email',
        on_delete=models.CASCADE
    )
    first_name = models.CharField(default='',max_length=50)
    last_name = models.CharField(default='',max_length=50)

    avatar_img = models.ImageField(blank=True,null=True,upload_to=upload_avatar_path)

    def __str__(self):
        return self.user_profile.username

