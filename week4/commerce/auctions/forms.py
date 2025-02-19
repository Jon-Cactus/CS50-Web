from django.forms import ModelForm
from .models import User, Listing, Bid, Comment

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "category", "image_URL", "starting_bid"]