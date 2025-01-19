from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.generate_entry, name="entry"),
    path("error", views.error, name="error"),
    path("add_entry", views.add_entry, name="add"),
]
