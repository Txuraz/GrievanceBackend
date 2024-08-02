from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from .sentiment_analysis import analyze_sentiment

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    vote = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(get_user_model(), related_name='upvoted_articles')
    downvoted_by = models.ManyToManyField(get_user_model(), related_name='downvoted_articles')
    is_completed = models.BooleanField(default=False)
    stay_anonymous = models.BooleanField(default=False)
    sentiment = models.CharField(max_length=20, default='neutral')

    def save(self, *args, **kwargs):
        self.sentiment = analyze_sentiment(self.content)
        super().save(*args, **kwargs)

        if self.is_completed:
            self.author.completed_article_count = Article.objects.filter(
                author=self.author, is_completed=True
            ).count()
            self.author.save()
