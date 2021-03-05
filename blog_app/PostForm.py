from .models import Posts
from django import forms
class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields=['title','content']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control'}),
        }