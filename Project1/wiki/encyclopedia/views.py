from django import forms
from django.shortcuts import render
import markdown
import random

from . import util


class NewPage(forms.Form):
    task = forms.CharField(label="New Task")

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def result(request, title):
    converting = convert_md_to_html(title)

    if converting == None:
        return render(request, "encyclopedia/error.html", {
            "errormessage": "This result does not exist."
        })
    else:
        return render(request, "encyclopedia/result.html", {
            "title": title,
            "result": converting
        })

def search(request):
    if request.method == "POST":
        entry_send = request.POST['q']
        converting = convert_md_to_html(entry_send)
        if converting is not None:
            return render(request, "encyclopedia/result.html", {
                "title": entry_send,
                "result": converting
            })
        else:
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if entry_send.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })

def newPage(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "errormessage": "This content already exists."
            })
        else:
            util.save_entry(title, content)
            converting = convert_md_to_html(title)
            return render(request, "encyclopedia/result.html", {
                "title": title,
                "result": converting
            })

def edit(request):
    if request.method =='POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "result": content
        })
    
def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        converting = convert_md_to_html(title)
        return render(request, "encyclopedia/result.html", {
            "title": title,
            "result": converting
        })

def rand(request):
    entries = util.list_entries()
    randlist = random.choice(entries)
    converting = convert_md_to_html(randlist)
    return render(request, "encyclopedia/result.html", {
        "title": randlist,
        "result": converting
    })