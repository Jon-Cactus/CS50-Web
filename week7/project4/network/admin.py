from django.contrib import admin
from .models import User, Post, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "timestamp")
    readonly_fields = ("get_likes",)

    def get_likes(self, obj):
        return ", ".join([user.username for user in obj.likes.all()])
    get_likes.short_description = "Likes"


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "get_following", "get_followers")
    readonly_fields = ("display_followers",)

    def get_following(self, obj):
        return ", ".join([user.username for user in obj.following.all()])
    get_following.short_description = "Following"

    def get_followers(self, obj):
        return ", ".join([user.username for user in obj.followers.all()])
    get_followers.short_description = "Followers"

    def display_followers(self, obj):
        return ", ".join([user.username for user in obj.followers.all()])
    display_followers.short_description = "Followers"

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "text", "timestamp")

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
