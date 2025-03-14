from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bid, Comment 
from .forms import ListingForm
from django.shortcuts import redirect
from .models import User


def index(request):
    listings = Listing.objects.all() #Have all listings ready

    return render(request, "auctions/index.html", {
        "listings": listings.filter(active=True)
    })

def categories(request, category=None):

    if category:
        listings = Listing.objects.filter(category=category)

        return render(request, "auctions/categories.html", {
            "listings": listings
        })
    else:
        categories = Listing.CATEGORY_CHOICES
        return render(request, "auctions/categories.html", {
            "categories": categories
        })

def login_view(request):
    if request.method == "POST":

        #Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        #Check if authentication successful
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

        #Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        #Attempt to create new user
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
    
@login_required    
def new_listing(request):
    if request.method == "POST": #When the user submits the new_listing form
        form = ListingForm(request.POST)
        if form.is_valid(): #Check if the form has been entirely filled out
           form.save()
           return redirect("listing", form.instance.id) #Take user to new listing
           
        else:
            print(form.errors)
            return render(request, "auctions/new-listing.html", {
                "form": form
            })

        
    #When the page is loaded via get
    form = ListingForm()
    return render(request, "auctions/new-listing.html", {
        "categories": Listing.CATEGORY_CHOICES,
        "form": form,
        
    })

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user

    if request.method == "POST" and request.user.is_authenticated:
        bid = request.POST.get("bid")
        text = request.POST.get("comment")
        end_auction = request.POST.get("end_auction")

        if bid:
            #Check if a highest bid exists
            highest_bid = listing.highest_bid.bid if listing.highest_bid else listing.starting_bid
            if int(bid) >= highest_bid:
                bid = Bid(bid=bid, user=user, listing=listing)
                bid.save()
                listing.highest_bid = bid
                listing.save()
            else: #case where user somehow input a bid lower than the highest bid
                return render(request, "auctions/error.html", {
                    "message": "Bid must be higher than the highest bid!"
                })

        elif text:
            comment = Comment(user=user, listing=listing, text=text)
            comment.save()

        elif end_auction:
            listing.active = False
            listing.winner = listing.highest_bid.user
            listing.save()
        
        else:
            return render(request, "auctions/error.html", {
                "message": "Login required"
            })
    
    comments = Comment.objects.filter(listing=listing).order_by('date')
    if request.user.is_authenticated:
        watchlist = user.watchlist.all()
    else:
        watchlist = None

    listing = Listing.objects.get(id=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": watchlist,
        "comments": comments,
    })

@login_required
def watchlist(request):
    user = request.user
    watchlist = user.watchlist.all()

    if request.method == "POST":
        listing_id = request.POST["listing"]
        listing = Listing.objects.get(id=listing_id)
        if listing in watchlist: #If listing in watchlist
            user.watchlist.remove(listing)
        else:
            user.watchlist.add(listing)

    watchlist = user.watchlist.all().order_by('date') #Load new watchlist so that changes are rendered        
    return render(request, "auctions/watchlist.html", {
        "user": user,
        "watchlist": watchlist
    })

def error(request):
    return render(request, "auctions/error.html")