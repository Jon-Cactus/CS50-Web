from django.contrib import admin
from .models import User, Post, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "likes", "timestamp")

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "following")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "text", "timestamp")

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
