from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers")
    saved_posts = models.ManyToManyField("Post", blank=True, related_name="saved_by")

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_posts")
    content = models.TextField(max_length=512, blank=False, null=False)
    likes = models.ManyToManyField("User", blank=True, related_name="liked_posts")
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def like_count(self):
        return self.likes.count()

class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    text = models.CharField(blank=False, null=False, max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)