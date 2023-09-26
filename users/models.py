from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    completed_article_count = models.PositiveIntegerField(default=0)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


User = get_user_model()


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"PasswordResetToken for {self.user.email}"

    def is_expired(self):
        now = timezone.localtime(timezone.now()).replace(tzinfo=None)
        return self.expires_at < now
