from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
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
    categorie_name = models.CharField(max_length=220,blank=False, null=False,default="None",unique=False)
    class Meta:
            db_table = 'categorie'
    def __str__(self):
        return self.categorie_name
    def get_absolute_url(self):
        return reverse("home")

class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=220,blank=False, null=False)
    #image=models.ImageField(default='http://0.gravatar.com/avatar/3f009d72559f51e7e454b16e5d0687a1?s=96&d=mm&r=g', upload_to='profile_pics')
    content=models.TextField(blank=True, null=True)
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
    content=models.TextField(blank=True, null=True)
    date_posted=models.DateTimeField(default=timezone.now)
    class Meta:
            db_table = 'comments'