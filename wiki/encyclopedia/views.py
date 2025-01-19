from django.shortcuts import render, redirect
from django.urls import reverse

from . import util


def index(request):
    # Entry search query
    if request.method == "GET" and 'q' in request.GET:
        entries = util.list_entries()
        q = request.GET.get('q')
        if q not in entries:
            return redirect(reverse('error', args=[q]))
        else:
            return redirect(reverse('entry', args=[q]))
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

"""
Need to complete generate_entry before index can be properly displayed
Next step: Create the html page for entries
"""
def generate_entry(request, entry):
    return render(request, f"encyclopedia/entry.html", {
        "entry": entry
    })

def add_entry(request):
    #TODO create an add.html and correctly tie it to the error view and error.html
    return False

def error(request, q):
    #TODO: create a redirect to add a page with the search query
    return render(request, "encyclopedia/error.html", {
        "q": q
    })
