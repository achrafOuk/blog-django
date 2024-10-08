from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render
from .models import Posts
from .models import Comments
from django.views.generic import (
    TemplateView,
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
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Blog CRUD classes
def get_categories():
    return Categories.objects.raw("""
        select categorie.categorie_id,count(*) as count,categorie.categorie_name as categorie from
         posts join categorie on posts.categorie_id=categorie.categorie_id 
         GROUP by `categorie_name`
         """)
class BlogList(ListView):
    model = Posts
    template_name = "index.html"
    ordering =['-date_posted']
    context_object_name="posts"
    paginate_by = 2
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['categories'] = get_categories()
        return context

class blogView(DetailView):
    model = Posts
    template_name = 'blog.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Posts.objects.get(post_id=self.kwargs['pk'])
        context['title']  = context['post'].title
        context['comments'] = Comments.objects.filter(post=context['post'].post_id)
        context['categories'] = get_categories()
        views_number = context['post'].views+1
        Posts.objects.filter(post_id=self.kwargs['pk']).update(views=views_number)
        context['author'] = User.objects.get(id=context['post'].author_id)
        context['img']= context['author'].profile.image.url 
        return context
    def post(self,request,**kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        post_id = context['post'].post_id
        name = request.POST['name']
        email = request.POST['email']
        comment = request.POST['body']
        date_posted = datetime.today().isoformat()
        comment = Comments(post_id=post_id,user=name,email=email,content=comment,date_posted=date_posted)
        comment.save()
        return self.render_to_response(context=context)
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
        context['title'] = 'Edit blog'
        context['role'] = 'Edit blog'
        return context
# End blog CRUD 
class About(BlogList):
    template_name = "about.html"
class Contact(BlogList):
    template_name = "contact.html"

def search(request):
    categories= get_categories()
    search_word = request.GET['fsearch']
    posts = Posts.objects.raw(f"SELECT * FROM `posts` WHERE title like '%%{search_word}%%'")
    posts = Posts.objects.filter(title__contains=search_word)
    search_word = search_word.replace(" ","+")
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    index = render_to_string('search.html', {"search":search_word,"categories":categories,"search_word":search_word,'title': 'APP', 'user': request.user,'posts':posts})
    return HttpResponse(index)
# categories CRUD
class NewCategorie(LoginRequiredMixin,CreateView,BlogList):
    model=Categories
    fields = ['categorie_name']
    template_name ="manage/new_categorie.html"
    def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)
class EditCategories(LoginRequiredMixin,UpdateView,BlogList):
    model = Categories
    template_name = "manage/new_blog.html"
    fields = ['categorie_name']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = 'Edit category name'
        return context
# Categories CRUD ends
def postsByCateogire(request,cat):
    categories= get_categories()
    cat = cat.replace("-", " ")
    categorie =Categories.objects.filter(categorie_name=cat).values_list("categorie_id")
    if categorie:
        categorie_id = categorie[0][0]
        categorie_posts = Posts.objects.filter(categorie_id=categorie_id).order_by('-date_posted')
        page = request.GET.get('page', 1)
        paginator = Paginator(categorie_posts, 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        data = {"title":cat,"categories":categories,"categorie":cat,"categorie_posts":posts}
        return render(request,"categorie_posts.html",data)
    return render(request,"categorie_posts.html")
# admin 
class AdminDashboard(LoginRequiredMixin,TemplateView):
    template_name = "admin/profile.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['visit_count'] = 100
        context['comments_count'] = 2
        return context
