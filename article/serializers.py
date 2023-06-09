

from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ArticleStatusUpdateSerializer(serializers.Serializer):
    is_completed = serializers.BooleanField()
