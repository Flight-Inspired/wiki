from django.shortcuts import render, redirect
from .util import get_entry, list_entries, delete_entry_util
import markdown
from django.template import loader
import random

from . import util


from django.shortcuts import render, redirect
from .util import get_entry, save_entry, delete_entry_util
import markdown
from . import util

def edit_page(request, title):
    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/error_page.html", {
            "error_message": "Entry does not exist"
        })

    if request.method == "POST":
        new_content = request.POST.get("content")

        if "delete" in request.POST:
            util.delete_entry_util(title)
            return redirect("index")

        if new_content is not None:
            util.save_entry(title, new_content)
            return redirect("entry_page", title=title)

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })



def random_page(request):
    entries = list_entries()
    if entries:
        random_entry = random.choice(entries)
        return redirect('entry_page', title=random_entry)
    else:
        return redirect('index')  

def entry_page(request, title=None):
    if not title:
        return random_page(request)

    entry_content = get_entry(title)
    if entry_content is None:
        return render(request, "encyclopedia/error_page.html", {
            "error_message": "Entry does not exist"
        })

    html_content = markdown.markdown(entry_content)

    return render(request, "encyclopedia/entry_page.html", {
        "title": title,
        "content": html_content
    })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        # Check if entry already exists
        if util.get_entry(title) is not None:
            return render(request, 'encyclopedia/error_page.html', {
                'error_message': 'Entry already exists with this title'
            })
        # Save the new entry
        util.save_entry(title, content)
        # Redirect to the newly created entry's page
        return redirect('entry_page', title=title)

    return render(request, 'encyclopedia/new_page.html')


def search_results(request):
    query = request.GET.get('q')
    matching_entries = [entry for entry in list_entries() if query.lower() in entry.lower()]
    print(query)
    if len(matching_entries) == 0:
        # No matching entries found, render a template showing search results
        return render(request, 'encyclopedia/search_results.html', {'query': query})
    elif len(matching_entries) == 1:
        # If there's a single matching entry, redirect to that entry page
        return redirect('entry_page', title=matching_entries[0])
    else:
        # Display the list of matching entries along with the query
        return render(request, 'encyclopedia/search_results.html', {'query': query, 'entries': matching_entries})


