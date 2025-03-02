from django.urls import path
from . import views

urlpatterns = [
    path("add_entry", views.add_entry, name="add_no_query"),
    path("add_entry/<str:search_query>", views.add_entry, name="add"),
    path("error/<str:entry_title>", views.error, name="error"),
    path("", views.index, name="index"),
    path("wiki/<str:entry_title>", views.generate_entry, name="entry"),
    path("wiki/random", views.generate_entry, name="entry_no_query"),
    path("results/<str:search_query>", views.results, name="results"),
]
