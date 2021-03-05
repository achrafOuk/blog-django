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
    views_number = post.views+1
    Posts.objects.filter(post_id=post_id).update(views=views_number)
    post_title  = post.title
    blog = render_to_string('blog.html', {'img':author.profile.image.url,'title': post_title,'author':str(author.username), 'user': request.user,'post':post})
    return HttpResponse(blog)

#@login_required
class NewBlog(LoginRequiredMixin,CreateView):
    model=Posts
    form_class =PostForm
    template_name ="manage/new_blog.html"
    def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)
