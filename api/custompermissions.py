from rest_framework import permissions


class ProfilePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # GETメソッドなどのセーフメソッドは許可する
        if request.method in permissions.SAFE_METHODS:
            return True
        # モデルのuserProがログインユーザーのidと一致する場合のみ許可する
        return obj.user.id == request.user.id
