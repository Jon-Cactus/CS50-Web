from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bid, Comment 
from .forms import ListingForm

from .models import User


def index(request):
    listings = Listing.objects.all() # have all listings ready

    return render(request, "auctions/index.html", {
        "listings": listings.filter(active=True)
    })
    


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def new_listing(request):
    if request.method == "POST": #when the user submits the new_listing form
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        image_URL = request.POST["image_URL"]
        starting_bid = request.POST["starting_bid"]
        listing_data = {
            "user": user,
            "title": title,
            "description": description,
            "category": category,
            "starting_bid": starting_bid
        }
        if image_URL: # handle case where image_URL is provided
            listing_data["image_URL"] = image_URL
        
        listing = Listing(**listing_data)
        listing.save()

    # When the page is loaded via get
    form = ListingForm()
    return render(request, "auctions/new-listing.html", {
        "categories": Listing.CATEGORY_CHOICES,
        "form": form,
        
    })

def listing(request):
    pass

    # if request.GET.get('sort'):
