from django.shortcuts import get_object_or_404
from posts.models import Follow, Group, Post
from rest_framework import mixins, permissions, viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

from .permissions import AuthorOrAuthenticatedReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class CustomListCreateViewSet(viewsets.GenericViewSet,
                              mixins.CreateModelMixin, mixins.ListModelMixin):
    pass


class PostViewSet(viewsets.ModelViewSet):
    """Получение и создание постов."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrAuthenticatedReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение группы."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination


class CommentViewSet(viewsets.ModelViewSet):
    """Получение комментариев поста и редактирование."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrAuthenticatedReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(CustomListCreateViewSet):
    """Получение и создание подписчиков."""
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
