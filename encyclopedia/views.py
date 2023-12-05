from django.shortcuts import render

from markdown2 import Markdown

from . import util

import random



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convert(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def entry(request, title):
    html_content = convert(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "content": "This message does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST":
        e_search = request.POST['q']
        html_content = convert(e_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": e_search,
                "content": html_content
            })
        else:
            recommend = []
            for entry in util.list_entries():
                if e_search.lower() in entry.lower():
                    recommend.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommend": recommend
            })

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html",{
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })

def edit(request):
    if request.method == 'POST':
        title = request.POST['e_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
def rand(request):
    rand_entry = random.choice(util.list_entries())
    html_content = convert(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "content": html_content
    })