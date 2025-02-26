from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist  = models.ManyToManyField("Listing", blank=True, related_name="watching_user")

class Listing(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="listings_created")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    CATEGORY_CHOICES = (
        ("msc", "Misc"),
        ("ctb", "Collectibles"),
        ("fnt", "Furniture"),
        ("fsh", "Fashion"),
        ("mrb", "Memorabilia"),
        ("spt", "Sports"),
        ("toy", "Toys"),
    )
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='msc')
    image_URL = models.URLField(null=True, blank=True)
    starting_bid = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="won_auctions")
    highest_bid = models.ForeignKey('Bid', null=True, blank=True, on_delete=models.CASCADE, related_name="current_highest_bids")
    

class Bid(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    text = models.CharField(max_length=512)
    date = models.DateTimeField(auto_now_add=True)
    