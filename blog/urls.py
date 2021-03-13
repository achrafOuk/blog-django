"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from blog_app import  views
from django.contrib.auth import views as auth_views
urlpatterns = [
path('', views.BlogList.as_view(), name='home'),
path('about/', views.About.as_view(),name='about'),
path('search', views.search,name='search'),
path('post/<int:post_id>', views.blog,name='post'),
path('post/new/', views.NewBlog.as_view(),name='new_blog'),
path('categorie/new/', views.NewCategorie.as_view(),name='new_categorie'),
path('contact/', views.Contact.as_view(),name='contact'),
path('admin/', admin.site.urls,name='home'),
path('login/', auth_views.LoginView.as_view(template_name='author/login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
]
from django.conf import settings
from django.conf.urls.static import static

"""urlpatterns = [
    # ... the rest of your URLconf goes here ...
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)"""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)