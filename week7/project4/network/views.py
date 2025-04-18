import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Comment

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
    
    post = Post(user=request.user, content=content)
    try:
        post.save()
    except Exception as e:
        return JsonResponse({"error": f"Failed to save post: {str(e)}"}, status=500)

    return JsonResponse({"message": "Post shared successfully.", "post_id": post.id}, status=201)

@csrf_exempt
@login_required
def edit_post(request, post_id):
    try: # Make sure post exists
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    # Handle the user manually inputting the URL to edit a post
    if post.user != request.user:
        return JsonResponse({"error": "You are not authorized to edit this post!"}, status=403)
    # Ensure this route is accessed only by PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    # grab all information from form object
    data = json.loads(request.body)
    updated_content = data.get("updatedContent")
    if updated_content is not None:
        post.content = updated_content
        post.save()
        return JsonResponse({
            "message": "Post updated successfully.",
            "post": {
                "content": post.content,
                "timestamp": post.timestamp.isoformat()
            }
        }, status=200)
    else:
        return JsonResponse({"error": "Can't save empty posts!"}, status=400)

def follow_user(request, user_id):
    try:
        user_to_be_followed = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"Error": "User not found."}, status=404)
    
    if request.method != "PUT":
        return JsonResponse({"Error": "PUT request required."}, status=400)
    

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
        query=Post.objects.select_related("user").order_by("-timestamp"),
        template="network/index.html",
        title="All Posts",
    )

@login_required
def following_posts(request):
    return post_paginator(
        request,
        query=Post.objects.select_related("user").filter(user__in=request.user.following.all()).order_by("-timestamp"),
        template="network/following.html",
        title="Following",
    )

def profile(request, username):
    user = User.objects.get(username=username)
    if not user:
        return False #TODO render error page
    
    return post_paginator(
        request,
        query=user.user_posts.select_related("user").order_by("-timestamp"),
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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
