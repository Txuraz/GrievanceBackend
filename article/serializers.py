from rest_framework import serializers
from .models import Article
#from .sentiment_analysis import analyze_sentiment
from .sentiment_analysis_vader_transformer import analyze_sentiment

class ArticleSerializer(serializers.ModelSerializer):
    sentiment = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'author', 'created_at', 'vote', 'upvoted_by', 'downvoted_by', 'is_completed')

    def get_sentiment(self, obj):
        return analyze_sentiment(obj.content)


class ArticleStatusUpdateSerializer(serializers.Serializer):
    is_completed = serializers.BooleanField()