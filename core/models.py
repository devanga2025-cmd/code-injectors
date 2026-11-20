from django.db import models
from django.contrib.auth.models import User

class DemoRequest(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    github_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    github_username = models.CharField(max_length=150, blank=True, null=True)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    provider = models.CharField(max_length=50, default='github')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.provider})"
