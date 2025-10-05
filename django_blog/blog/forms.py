from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag

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



class PostModelForm(forms.ModelForm):
    # text input where author types: "django, python, web"
    tags = forms.CharField(
        required=False,
        help_text="Comma-separated tags (e.g. django, python)",
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title here'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your post...'}),
        }

    def __init__(self, *args, **kwargs):
        # when editing, set initial tags field to a comma-separated string
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = ', '.join([t.name for t in self.instance.tags.all()])

    def clean_tags(self):
        raw = (self.cleaned_data.get('tags') or '').strip()
        if not raw:
            return []
        # split by comma and normalize: strip spaces, lower-case
        tag_names = [t.strip() for t in raw.split(',') if t.strip()]
        # normalize duplicates and lower-case for uniqueness
        normalized = []
        for tn in tag_names:
            if tn.lower() not in [n.lower() for n in normalized]:
                normalized.append(tn)
        return normalized

    def save(self, commit=True):
        # pop tags from cleaned_data and handle them separately
        tags = self.cleaned_data.pop('tags', [])
        post = super().save(commit=commit)
        # If commit was False, instance might not be saved; ensure it has a pk
        if commit:
            # clear existing tags and add the new/existing Tag objects
            post.tags.clear()
            for name in tags:
                tag_obj, created = Tag.objects.get_or_create(name=name)
                post.tags.add(tag_obj)
        else:
            # if commit=False, save() caller must later call post.save() and then handle tags
            # But for our views we call save(commit=True) so this is fine.
            pass
        return post