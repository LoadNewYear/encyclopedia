from django.shortcuts import render, HttpResponse, redirect, reverse
from django import forms

from . import util

from markdown import markdown
import random



# Create the Django class for creating a form form creating a new entry
class NewEntryForm(forms.Form):
    Entry_Title = forms.CharField(label="New Entry", widget=forms.TextInput(attrs={'class': 'form-label'}))
    Entry_Description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput())



# Entry function that returns a list of entries
def index(request):
    search_form = SearchForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": search_form
    })


# Function that gets the description of an entry using it's title
def displayPage(request, TITLE):
    entries = util.list_entries()
    if TITLE in entries:
        return render(request, "encyclopedia/wiki/page.html", {
            "pager": TITLE.capitalize(),
            "desc": markdown(util.get_entry(TITLE)),
        })
    else:
        return HttpResponse(f"Could not find any page with the name {TITLE}")


# If this function gets a GET request it gives the new.html page form and should warn variables
# When it gets a POST request it creates a new entry
def new(request):
    search_form = SearchForm()
    should_warn = False
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            form_title =  form.cleaned_data["Entry_Title"]
        form_description = form.cleaned_data["Entry_Description"]
        if form_title in util.list_entries():
            should_warn = True
        else:
            util.save_entry(form_title, form_description)
    return render(request, "encyclopedia/new.html", {
        "form" : NewEntryForm(),
        "should_warn": should_warn,
        "search_form": search_form
    });


def search(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            lst = []
            data = search_form.cleaned_data["query"]
            for entry in util.list_entries():
                if data.lower() in entry.lower():
                    print(entry)
                    lst.append(entry)
                    # if there are no pages with that substring then error page is shown
            if len(lst) == 0:
                content = "The page you requested is not available"
                return HttpResponse(content)
                        # if there are pages with that substring then they are listed
            else:
                return render(request, "encyclopedia/index.html", {"entries": lst, "search_form": search_form})



def randomPage(request):
    entries = util.list_entries()
    x = random.randrange(0, len(entries))
    url = reverse('displayPage', args=[entries[x]])
    return redirect(url)
