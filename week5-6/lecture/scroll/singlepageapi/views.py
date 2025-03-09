from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.

def index(request):
    return render(request, "singlepage/index.html")

texts = [
    "This is test text for 1",
    "If this text shows for 2 then we might have this thing working",
    "Final test text. If this works, then it works!"
]

def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num - 1])
    else:
        raise Http404("No such section")