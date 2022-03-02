from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор модели группы."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    """Сериализатиор модели постов."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'text',
            'pub_date',
            'image',
            'group'
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        model = Comment
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор модели комменатриев."""
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate_following(self, value):
        if self.context.get('request').user == value:
            raise serializers.ValidationError(
                'Пользователь не может подписываться на себя!'
            )
        return value