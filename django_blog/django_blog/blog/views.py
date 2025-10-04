from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    # fetch posts ordered by newest first
    posts = Post.objects.order_by('-published_date')
    # render 'blog/post_list.html' with the posts in the context
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    # return 404 if post not found
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
