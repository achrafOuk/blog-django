from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render
from .models import Posts
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponse
from django.template.loader import render_to_string
from .PostForm import PostForm
from django.contrib.auth.models import User
def index(request):
    posts = Posts.objects.all()  
    index = render_to_string('index.html', {'title': 'APP', 'user': request.user,'posts':posts})
    return HttpResponse(index)

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")
def blog(request,post_id):
    post = Posts.objects.get(post_id=post_id)  
    author = User.objects.get(id=int(post.author_id))
    blog = render_to_string('blog.html', {'title': 'APP','author':str(author.username), 'user': request.user,'post':post})
    return HttpResponse(blog)
class NewBlog(CreateView):
    model=Posts
    form_class =PostForm
    template_name ="manage/new_blog.html"
    #fields = ['title', 'content']
    #redirect('home')