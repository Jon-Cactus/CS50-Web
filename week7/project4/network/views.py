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

def post_paginator(request, query, template, title):
    # https://docs.djangoproject.com/en/5.1/ref/models/querysets/#select-related , acts like an SQL `JOIN`
    paginator = Paginator(query.select_related("user").order_by("-timestamp"), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, template, {
        "page_obj": page_obj,
        "title": title
    })
def index(request):

    return post_paginator(
        request,
        query=Post.objects.all(),
        template="network/index.html",
        title="All Posts"
    )

@login_required
def following(request):
    
    return post_paginator(
        request,
        query=Post.objects.filter(user__in=request.user.following.all()),
        template="network/following.html",
        title="Following"
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
