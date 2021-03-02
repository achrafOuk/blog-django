from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template.loader import render_to_string


def index(request):
    posts = [
        {
            'author': 'CoreyMS',
            'title': 'Blog Post 1',
            'content': 'First post content',
            'date_posted': 'August 27, 2018'
        },
        {
            'author': 'Jane Doe',
            'title': 'Blog Post 2',
            'content': 'Second post content',
            'date_posted': 'August 28, 2018'
        }
    ]
    index = render_to_string('index.html', {'title': 'APP', 'user': request.user,'posts':posts})
    return HttpResponse(index)

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")
