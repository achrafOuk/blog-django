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

class blogView(DetailView):
    model = Posts
    template_name = 'blog.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Posts.objects.get(post_id=self.kwargs['pk'])
        post_title  = context['post'].title
        context['comments'] = Comments.objects.filter(post=context['post'].post_id)
        context['categories']= Categories.objects.all()
        context['author'] = User.objects.get(id=context['post'].author_id)
        context['img']= context['author'].profile.image.url 
        return context

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

class NewCategorie(LoginRequiredMixin,CreateView,BlogList):
    model=Categories
    fields = ['categorie_name']
    template_name ="manage/new_categorie.html"
    def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)