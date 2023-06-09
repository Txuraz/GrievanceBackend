

from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'author', 'created_at', 'vote', 'upvoted_by', 'downvoted_by', 'is_completed')


class ArticleStatusUpdateSerializer(serializers.Serializer):
    is_completed = serializers.BooleanField()
