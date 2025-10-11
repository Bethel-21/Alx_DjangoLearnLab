from rest_framework import viewsets, permissions, filters, status
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: only owners can edit/delete their posts/comments.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # set author automatically


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # set author automatically


class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Get users that the current user is following
        following_users = user.following.all()
        # Get posts from those users
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        # Check if the user already liked this post
        if Like.objects.filter(post=post, user=request.user).exists():
            return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        like = Like.objects.create(post=post, user=request.user)
        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(post=post, user=request.user).first()
        if like:
            like.delete()
            return Response({"detail": "Like removed."}, status=status.HTTP_200_OK)
        return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)