from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment

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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'})
        }

    def clean_content(self):
        content = (self.cleaned_data.get('content') or '').strip()
        if not content:
            raise forms.ValidationError("Comment can't be empty.")
        if len(content) > 3000:
            raise forms.ValidationError("Comment is too long.")
        return content