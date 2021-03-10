from django.contrib.auth.decorators import login_required
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
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Categories
def index(request):
    posts = Posts.objects.all().order_by('-date_posted')   
    index = render_to_string('index.html', {'title': 'APP', 'user': request.user,'posts':posts})
    return HttpResponse(index)

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")
def blog(request,post_id):
    post = Posts.objects.get(post_id=post_id)
    author = User.objects.get(id=int(post.author_id))
    views_number = post.views+1
    Posts.objects.filter(post_id=post_id).update(views=views_number)
    post_title  = post.title
    blog = render_to_string('blog.html', {'img':author.profile.image.url,'title': post_title,'author':str(author.username), 'user': request.user,'post':post})
    return HttpResponse(blog)

def search_blog(request,search_word):
    #posts = Posts.objects.raw(f"select * from posts where title like '%{search_word}%'").order_by('-date_posted')   
    posts = Posts.objects.raw(f"SELECT * FROM `posts` WHERE title like '%%{search_word}%%'")
    index = render_to_string('index.html', {'title': 'APP', 'user': request.user,'posts':posts})
    return HttpResponse(index)

class NewBlog(LoginRequiredMixin,CreateView):
    model=Posts
    fields = ['title', 'content', 'keywords', 'categorie']
    template_name ="manage/new_blog.html"
    def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)
class NewCategorie(LoginRequiredMixin,CreateView):
    model=Categories
    fields = ['categorie_name']
    template_name ="manage/new_categorie.html"
    def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)