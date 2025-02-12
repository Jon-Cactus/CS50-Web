from django.urls import path
from . import views

# This connects and routes each of this app's (newyear) views
urlpatterns = [
    path("", views.index, name="index"),
]