from .models import Posts
from django import forms
from .models import Categories
class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields=['title','content']
        categories = Categories.objects.all()
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control'}),
            'categories':forms.Select(choices=categories,attrs={'class':'form-control','placeholder':"categories"}),
            'keywords':forms.TextInput(attrs={'class':'form-control'}),
        }