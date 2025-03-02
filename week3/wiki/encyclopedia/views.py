from django.shortcuts import render, redirect
from django.urls import reverse
import markdown2, random, math
from . import util

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
    action = request.GET.get('action')
    entries = util.list_entries()

    if action == "random":
        random_index = math.floor(random.uniform(0, len(entries)))
        entry_title = entries[random_index] # Get random entry
        entry_content = util.get_entry(entry_title)
        return render(request, "encyclopedia/entry.html", {
            "entry_content": markdown2.markdown(entry_content),
            "entry_title": entry_title
        })
    
    if entry_title not in entries:
        return redirect(reverse('results', args=[entry_title]))
    entry_content = util.get_entry(entry_title)
    return render(request, "encyclopedia/entry.html", {
        "entry_content": markdown2.markdown(entry_content),
        "entry_title": entry_title
    })

def add_entry(request, search_query=None):

    # If submitting add or edit form
    if request.method == "POST":
        action = request.POST.get('action') #Determine which form was submitted
        entry_content = request.POST.get('entry_content').strip()
        entry_title = request.POST.get('entry_title').strip()

        if not entry_title or not entry_content:
            return render(request, "encyclopedia/error.html", {
                "error_message": "Title and content are required"
            })

        entries = util.list_entries()

        if action == "edit":
            util.save_entry(entry_title, entry_content)
            return redirect(reverse('entry', args=[entry_title]))
        
        if action == "add":
            if entry_title in entries:
                return redirect(reverse('error', args=[entry_title]))
            util.save_entry(entry_title, entry_content)
            return redirect(reverse('entry', args=[entry_title]))

    else: #GET request handling
        action = request.GET.get('action')
        entry_title = request.GET.get('entry_title', "")
        entry_content = util.get_entry(entry_title) if entry_title else ""

        if action == 'add':
            return render(request, "encyclopedia/add.html", {
                "action": "add",
                "search_query": search_query
            })
        
        if action == 'edit' and entry_title:
            return render(request, "encyclopedia/add.html", {
                "action": "edit",
                "entry_title": entry_title,
                "entry_content": entry_content
            })
        
         # If the user has been redirected by searching
        return render(request, "encyclopedia/add.html", {
            "search_query": search_query
        })
    

def results(request, search_query=None):
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

def error(request, entry_title):
    return render(request, 'encyclopedia/error.html', {
        "entry_title": entry_title
    })