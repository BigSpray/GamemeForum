from rest_framework import serializers
from .models import images, videos


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = images
        fields = ['id', 'img']


class VideosSerializer(serializers.ModelSerializer):

    class Meta:
        model = videos
        fields = ['id', 'video']