from django.shortcuts import render, redirect
from django.urls import reverse

from . import util

#TODO check variable names for potential refactors
def index(request):
    # Entry search query
    if 'q' in request.GET:
        entries = util.list_entries()
        search_query = request.GET.get('q')
        if search_query not in entries:
            return redirect(reverse('error', args=[search_query]))
        else:
            return redirect(reverse('entry', args=[search_query]))
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

def add_entry(request, search_query=None):
    #TODO create an add.html and correctly tie it to the error view and error.html
    if search_query is not None:
        return render(request, "encyclopedia/add.html", {
            "search_query": search_query
        })
    else:
        return render(request, "encyclopedia/add.html")

def error(request, search_query=None):
    #TODO: create a redirect to add a page with the search query

    return render(request, "encyclopedia/error.html", {
        "search_query": search_query
    })

def save(request):
    return False
