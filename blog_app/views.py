from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render
from .models import Posts
from .models import Comments
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from django.http import HttpResponse
from django.template.loader import render_to_string
from .PostForm import PostForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Categories
from django.views.generic import ListView
from django.contrib.auth import views as auth_views
from django.shortcuts import get_object_or_404
def index(request):
    posts = Posts.objects.all().order_by('-date_posted')   
    index = render_to_string('index.html', {'title': 'APP', 'user': request.user,'posts':posts})
    return HttpResponse(index)
# Blog CRUD classes
class BlogList(ListView):
    model = Posts
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['posts'] = Posts.objects.all().order_by('-date_posted')   
        context['categories'] = Categories.objects.all()
        return context
def blog(request,post_id):
    post = Posts.objects.get(post_id=post_id)
    author = User.objects.get(id=int(post.author_id))
    comments = Comments.objects.filter(post=int(post_id))
    categories= Categories.objects.all()
    views_number = post.views+1
    Posts.objects.filter(post_id=post_id).update(views=views_number)
    post_title  = post.title
    blog = render_to_string('blog.html', {'categories':categories,'comments':comments,'img':author.profile.image.url,'title': post_title,'author':str(author.username), 'user': request.user,'post':post})
    return HttpResponse(blog)

class NewBlog(LoginRequiredMixin,CreateView,BlogList):
    model=Posts
    fields = ['title', 'content', 'keywords', 'categorie']
    template_name ="manage/new_blog.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = 'Create new blog'
        return context
class EditBlog(LoginRequiredMixin,UpdateView,BlogList):
    model = Posts
    fields = ['title', 'content', 'keywords', 'categorie']
    template_name = "manage/new_blog.html"
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = 'Edit blog'
        return context

class About(BlogList):
    template_name = "about.html"
class Contact(BlogList):
    template_name = "contact.html"

def search(request):
    #posts = Posts.objects.raw(f"select * from posts where title like '%{search_word}%'").order_by('-date_posted')   
    search_word = request.GET['fsearch']
    posts = Posts.objects.raw(f"SELECT * FROM `posts` WHERE title like '%%{search_word}%%'")
    categories = Categories.objects.all()
    index = render_to_string('index.html', {"categories":categories,"search_word":search_word,'title': 'APP', 'user': request.user,'posts':posts})
    return HttpResponse(index)

class NewCategorie(BlogList,LoginRequiredMixin,CreateView):
    model=Categories
    fields = ['categorie_name']
    template_name ="manage/new_categorie.html"
    def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)