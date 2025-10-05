from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

# Custom registration form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # add email field

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # author and published_date are set automatically
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title here'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your post...'}),
        }