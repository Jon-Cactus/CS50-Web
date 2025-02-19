from django.contrib import admin
from .models import User, Listing, Bid, Comment
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "category", "active", "winner", "highest_bid")
    list_filter = ("category", "active", "highest_bid")
    search_fields = ("user", "title")

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist",)


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
