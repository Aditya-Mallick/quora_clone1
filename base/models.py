from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200)
    bio = models.CharField(max_length=300, blank=True, null=True, default="")
    avatar = models.ImageField(
        default='avatar.svg', upload_to='images/', null=True, blank=True)
    credential = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=200, blank=True, null=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body


class Answer(models.Model):
    ques = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_answer = models.BooleanField(default=True)

    def __str__(self):
        return self.body[:50]


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='', blank=True, null=True)
    body = models.TextField(blank=False)
    is_answer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.title:
            return f"{self.title} -> {self.user}"
        return f"{self.user.username}'s Post"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ques = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ques.body


class FollowUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')

    def __str__(self):
        return f'{self.follower.username} follows {self.user.username}'
