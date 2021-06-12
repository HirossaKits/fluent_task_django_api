from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

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

    objects = UserManager()

    # emailをユーザー名として使用
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
