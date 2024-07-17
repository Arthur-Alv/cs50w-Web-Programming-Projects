from django.shortcuts import render
import markdown

from . import util


def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    entries = util.list_entries
    css_file = util.get_entry("CSS")
    coffee = util.get_entry("coffee")
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


