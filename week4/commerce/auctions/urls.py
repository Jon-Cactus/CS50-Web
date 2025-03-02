from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category>", views.categories, name="categories"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing", views.new_listing, name="new_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("error", views.error, name="error"),
]
