from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # If the article is completed, update the completed_article_count for the author
        if self.is_completed:
            self.author.completed_article_count = Article.objects.filter(
                author=self.author, is_completed=True
            ).count()
            self.author.save()