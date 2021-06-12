from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id','email','password')
        # write_onlyで登録、更新時のみ使用でき、シリアル化するときにフィールドに含まれないようにする
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user