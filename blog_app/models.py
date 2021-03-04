from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=220,blank=False, null=False)
    content=models.TextField(blank=True, null=True)
    date_posted=models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class Meta:
            db_table = 'posts'

class Comments(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.SET_NULL, null=True)
    content=models.TextField(blank=True, null=True)
    date_posted=models.DateTimeField(default=timezone.now)
    class Meta:
            db_table = 'comments'