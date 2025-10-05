from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostModelForm


def post_list(request):
    # fetch posts ordered by newest first
    posts = Post.objects.order_by('-published_date')
    # render 'blog/post_list.html' with the posts in the context
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    # return 404 if post not found
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# Registration view
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log user in after registration
            return redirect("profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})

# Login view
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
    else:
        form = AuthenticationForm()
    return render(request, "blog/login.html", {"form": form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect("login")

# Profile view
@login_required
def profile_view(request):
    if request.method == "POST":
        user = request.user
        user.email = request.POST.get("email", user.email)
        user.save()
    return render(request, "blog/profile.html")




# ListView: shows all posts, accessible to everyone
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # explicit template path
    context_object_name = 'posts'
    ordering = ['-published_date']  # newest first
    paginate_by = 10  # optional, change as desired

# DetailView: shows a single post, accessible to everyone
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# CreateView: only authenticated users can create posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostModelForm
    template_name = 'blog/post_form.html'
    # Where to send user after successful create, reverse to detail view using PK in form_valid
    def form_valid(self, form):
        # set the author to the current logged-in user before saving
        form.instance.author = self.request.user
        return super().form_valid(form)

# UpdateView: only the post's author can edit
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        # allow only the author to edit
        post = self.get_object()
        return post.author == self.request.user

# DeleteView: only the post's author can delete
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')  # go back to list after deletion

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
