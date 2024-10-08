from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from ckeditor.fields import RichTextField
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(blank=True, null=True)
    def __str__(self):
        return f'{self.user.username} Profile'
    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
class Categories(models.Model):
    categorie_id = models.AutoField(primary_key=True)
    categorie_name = models.CharField(max_length=220,blank=False, null=False,default="None",unique=True)
    def __str__(self):
        return self.categorie_name
    class Meta:
            db_table = 'categorie'
    def get_absolute_url(self):
        return reverse("home")

class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=220,blank=False, null=False)
    content=RichTextField(blank=True, null=True)
    date_posted=models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    views =models.IntegerField(default=0)
    categorie = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    keywords=models.CharField(max_length=220,blank=False, null=True)
    class Meta:
            db_table = 'posts'
    def get_absolute_url(self):
        return reverse("post", kwargs={"post_id": self.post_id})

class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE , null=True)
    user=models.CharField(max_length=220,blank=False, null=False,default="None")
    email=models.CharField(max_length=220,blank=False, null=False,default="None")
    content=models.TextField(blank=True, null=True)
    date_posted=models.DateTimeField(default=timezone.now)
    class Meta:
            db_table = 'comments'
    