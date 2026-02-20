from rest_framework import serializers
from .models import user, userData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['id', 'name', 'img', 'account', 'password', 'myself']


class UserDataSerializer(serializers.ModelSerializer):
    userID = UserSerializer(many=False)

    class Meta:
        model = userData
        fields = ['id', 'userID', 'content', 'video']


class UserShowDataSerializer(serializers.ModelSerializer):
    user_id = UserDataSerializer(many=True)

    class Meta:
        model = user
        fields = ['id', 'name', 'user_id']
