import markdown2
from random import choice
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util

## #create add  encyclopedia form model
class NewwikiForm(forms.Form):
    title = forms.CharField(label="page title",widget= forms.TextInput(attrs={'class':'form-control','id':'some_id'}))
    content = forms.CharField(label="page content",widget = forms.Textarea(attrs={'class':'form-control','id':'text','rows':'20'}))

def index(request):

    search_list = []
     
    ##if method is post
    if request.method == "POST":
        ##query for the encyclopedia entry
        title = request.POST["q"]
        if util.get_entry(title):
            return HttpResponseRedirect(f"{reverse(index)}wiki/{title}")
        else:
            ##if  encyclopedia entry dosen't exsist search for simlier  encyclopedias

            ##query all  encyclopedia entries
            titles = util.list_entries()
            
            ##search case insenstive  
            for i in titles:
                if i.lower() in title.lower() or title.lower()  in i.lower():
                    search_list.append(i)
                

            return render(request, "encyclopedia/index.html", {
                "search_list": search_list
                })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#add encyclopedia entry
def add(request):
    if request.method == "POST":
        form = NewwikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse(index))
        else:
            return render(request, "encyclopedia/add.html", {
                "form" :  NewwikiForm(),
                 "error" : "invaid input"})

            
    return render(request, "encyclopedia/add.html", {
         "form" :  NewwikiForm()
         })

#view encyclopedia entry
def view(request, name):

    content = util.get_entry(name)

    if not content:
        return render(request, "encyclopedia/view.html", {
            "title" : name,
             'error': 'this page does nor exsist consider adding it '
             })

    else:
        return render(request, "encyclopedia/view.html", {
            "title" : name,
            ##translate makedown syntax to html before sending it to user
             "content" : markdown2.markdown(content)
             })


#Edit encyclopedia entry
def edit(request, name):
    
    ##if method is post
    if request.method == "POST":
        form = NewwikiForm(request.POST)
        ##check if form input is valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            ##save changes
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse(index))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form" :  NewwikiForm(),
                 "error" : "invaid input"})

    ##else if user ask to edit encyclopedia

    ##query for the name of the encyclopedia
    content = util.get_entry(name)

    ##if entry has content
    if content:
        ##fill a form with that content and send it to user 
        data_dict = {'title': name , 'content': content }
        form = NewwikiForm(data_dict)
        return render(request, "encyclopedia/edit.html", {
        "title" : name,
        "form" : form
        })
        ##else send an error message
    else:
        data_dict = {'title': name , 'content': content }
        form = NewwikiForm(data_dict)
        return render(request, "encyclopedia/edit.html", {
        "title" : name,
        "form" : form,
        'error' : 'page does not exsist consider adding it '
        })

# random encyclopedia entry
def random(requst):
    list = util.list_entries()
    title = choice(list)
    return HttpResponseRedirect(f"{reverse(index)}wiki/{title}")
