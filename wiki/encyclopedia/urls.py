from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry_title>", views.generate_entry, name="entry"),
    path("results/<str:search_query>", views.results, name="results"),
    path("add_entry", views.add_entry, name="add_no_query"),
    path("add_entry/<str:search_query>", views.add_entry, name="add"),
    path("save/<str:entry_name", views.add_entry, name="save")
]
