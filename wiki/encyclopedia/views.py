from django.shortcuts import render, redirect
from django.urls import reverse
import markdown2
from . import util

#TODO check variable names for potential refactors
def index(request):
    # Entry search query
    if 'q' in request.GET:
        entries = util.list_entries()
        search_query = request.GET.get('q')
        if search_query not in entries:
            return redirect(reverse('results', args=[search_query]))
        else:
            return redirect(reverse('entry', args=[search_query]))
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def generate_entry(request, entry_title):
    entry_content = util.get_entry(entry_title)
    return render(request, "encyclopedia/entry.html", {
        "entry_content": markdown2.markdown(entry_content)
    })

def add_entry(request, search_query=None):
    if 'entry_text' in request.POST:
        entry_text = request.POST.get('entry_text')
        util.save_entry(search_query, entry_text)
    if search_query is not None:
        return render(request, "encyclopedia/add.html", {
            "search_query": search_query
        })
    else:
        return render(request, "encyclopedia/add.html")

def results(request, search_query=None):
    #TODO: List entries that fit the search query as a substring
    results = []
    entries = util.list_entries()
    for entry in entries:
        if search_query.lower() in entry.lower():
            results.append(entry)
    if len(results) > 0:
        return render(request, "encyclopedia/results.html", {
            "search_query": search_query,
            "results": results
        })
    else:
        return render(request, "encyclopedia/results.html", {
            "search_query": search_query
        })
