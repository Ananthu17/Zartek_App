from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from user_backend.models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields=['images','description','created_date','tags','likes','dislikes']
        widgets={
            'images':forms.FileInput(attrs={"class":"custom-file-input","id":"customFile",}),
            'description':forms.TextInput(attrs={'class': 'form-control','placeholder':'Add Description'}),
            'tags':forms.Select(attrs={'class':"js-example-basic-multiple",'multiple':"multiple"}),
        }