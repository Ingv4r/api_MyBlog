from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Comment, Follow, Group, Post

from .permissions import AuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """
    Provides custom view set methods for Post model
    with pagination.
    """

    queryset = Post.objects.select_related('author')
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        """Create custom method with author save."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Provides custom view set methods for Comment model."""

    queryset = Comment.objects.select_related('author')
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        """Create custom method with author and post-instance save."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        """Get custom queryset method."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        new_queryset = post.comments.all()
        return new_queryset


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Provides standart view set methods for Group model."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    """
    Provides custom GET and POST methods for Follow model
    with search filter.
    """

    queryset = Follow.objects.select_related('user')
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        """Create custom method with user field."""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Get custom queryset method with current user subscriptions."""
        new_queryset = Follow.objects.filter(
            user=self.request.user
        ).select_related('user')
        return new_queryset
