import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import User, Profile, Post, Comment

@csrf_exempt
@login_required
def share_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # grab all information from form object
    data = json.loads(request.body)
    content = data.get("content", "").strip() # isolate content
    if not content:
        return JsonResponse({"error": "Can't share empty posts!"}, status=400)
    
    post = Post(profile=request.user.profile, content=content)
    try:
        post.save()
    except Exception as e:
        return JsonResponse({"error": f"Failed to save post: {str(e)}"}, status=500)

    return JsonResponse({"message": "Post shared successfully.", "post_id": post.id}, status=201)

@csrf_exempt
@login_required
def edit_post(request, post_id):
    # Ensure this route is accessed only by PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    # Ensure post exists
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    #  Prevent the user from manually inputting the URL to edit a post
    if post.profile.user != request.user:
        return JsonResponse({"error": "You are not authorized to edit this post!"}, status=403)
    # grab all information from form object
    data = json.loads(request.body)
    updated_content = data.get("updatedContent")
    if updated_content is not None: # Ensure form is not empty
        post.content = updated_content
        post.edited_timestamp = timezone.now()
        post.save()
        return JsonResponse({
            "message": "Post updated successfully.",
            "post": {
                "content": post.content,
                "timestamp": post.timestamp.isoformat(),
                "edited_timestamp": post.edited_timestamp.isoformat() if post.edited_timestamp else None
            }
        }, status=200)
    else:
        return JsonResponse({"error": "Can't save empty posts!"}, status=400)

@csrf_exempt
@login_required
def toggle_follow(request, username):
    # Ensure this route is accessed only by put
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    try: # Ensure post exists
        target_user = Profile.objects.get(user__username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
    profile = request.user.profile
    if profile == target_user: # Check if the profile has manually entered the URL to follow themself
        return JsonResponse({"error": "Cannot follow yourself!"}, status=400)
    # Check for follow or unfollow
    if profile.following.filter(id=target_user.id).exists():
        profile.following.remove(target_user)
        return JsonResponse({"message": f"Unfollowed {username}", "following": False, "follower_count": target_user.follower_count}, status=200)
    profile.following.add(target_user)
    return JsonResponse({"message": f"Followed {username}", "following": True, "follower_count": target_user.follower_count}, status=200)

@csrf_exempt
@login_required
def like_post(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    # Add or remove the user from the post's likes
    profile = request.user.profile
    if post.likes.filter(id=profile.id).exists():
        post.likes.remove(profile)
        return JsonResponse({"message": "Unliked post!", "is_liked": False, "like_count": post.like_count}, status=200)
    post.likes.add(profile)
    return JsonResponse({"message": "Liked post!", "is_liked": True, "like_count": post.like_count}, status=200)

def post_paginator(request, query, template, title, user_obj=None):
    paginator = Paginator(query, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, template, {
        "page_obj": page_obj,
        "title": title,
        "user_obj": user_obj
    })

def index(request):
    return post_paginator(
        request,
        # https://docs.djangoproject.com/en/5.1/ref/models/querysets/#select-related , acts like an SQL `JOIN` for M
        query=Post.objects.select_related("profile").order_by("-timestamp"),
        template="network/index.html",
        title="All Posts",
    )

@login_required
def following_posts(request):
    return post_paginator(
        request,
        query=Post.objects.select_related("profile").filter(profile__in=request.user.profile.following.all()).order_by("-timestamp"),
        template="network/following.html",
        title="Following",
    )

def profile(request, username):
    user = User.objects.get(username=username)
    if not user:
        return False #TODO render error page
    
    return post_paginator(
        request,
        query=user.profile.post_set.select_related("profile").order_by("-timestamp"),
        template="network/profile.html",
        title=f"{user.username}'s Profile",
        user_obj=user
        )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            Profile.objects.create(user=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
