from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "practice/index.html")

def greet(request, name):
    return render(request, "practice/greet.html", {
        "name": name.capitalize(),
    })