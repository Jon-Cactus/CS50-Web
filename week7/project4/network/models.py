from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OnetoOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers")
    saved_posts = models.ManyToManyField("Post", blank=True, related_name="saved_by")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    profile_picture_url = models.URLField(blank=True, null=True)

    @property
    def following_count(self):
        return self.following.count()

    @property
    def follower_count(self):
        return self.followers.count()
    
    @property
    def display_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        elif self.profile_picture_url:
            return self.profile_picture_url
        return '/static/images/default_pic.jpg' # Default if user has not uploaded a picture

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_posts")
    content = models.TextField(max_length=512, blank=False, null=False)
    likes = models.ManyToManyField("Profile", blank=True, related_name="liked_posts")
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def comment_count(self):
        return self.comment_set.count()

class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    text = models.CharField(blank=False, null=False, max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)