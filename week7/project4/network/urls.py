
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following_posts, name="following_posts"),
    path("profile/<str:username>", views.profile, name="profile"),

    # API Routes
    path("post", views.share_post, name="post"),
    path("post/<int:post_id>", views.edit_post, name="edit_post"),
    path("profile/<str:username>/follow-toggle", views.toggle_follow, name="toggle_follow")
]
