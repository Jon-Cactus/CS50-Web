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
        "entry_content": markdown2.markdown(entry_content),
        "entry_title": entry_title
    })

def add_entry(request, search_query=None):

    # If submitting add or edit form
    if request.method == "POST":
        action = request.POST.get('action') #Determine which form was submitted
        entry_text = request.POST.get('entry_text')
        entry_title = request.POST.get('entry_title')

        # If the user properly input both fields
        if entry_title is not None and entry_text is not None:
            if action == 'edit':
                util.save_entry(entry_title, entry_text)
                return redirect(reverse('entry', args=[entry_title]))
            elif action == 'add':
                entries = util.list_entries()

                # Does the entry already exist?
                if entry_title not in entries:
                    util.save_entry(entry_title, entry_text)
                    return redirect(reverse('entry', args=[entry_title]))
                else:
                    return redirect(reverse('error', args=[entry_title]))      
        elif entry_title is None:
            #TODO 
            return False
        elif entry_text is None:
            #TODO
            return False
        
    # if get request
    else:
        action = request.GET.get('action') # Determine whether the user wants to add or edit
        edit_title = request.GET.get('edit_title')
        entry_content = util.get_entry(edit_title) if edit_title else ""
        # If the user clicked "Create New Page"
        if action == 'add':
            return render(request, "encyclopedia/add.html", {
                "action": action
            })
        
        # If the user clicks "edit"
        # Not working properly
        elif action == 'edit':
            # Debug
            print(f"Edit title: {edit_title}")
            print(entry_content)
            return render(request, "encyclopedia/add.html", {
                "action": action,
                "entry_title": edit_title,
                "entry_content": markdown2.markdown(entry_content)
            })
        
        # If the user has been redirected by searching
        else:
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