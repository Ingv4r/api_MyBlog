import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import exceptions, serializers, validators

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        allow_null=True,
    )

    class Meta:
        model = Follow
        fields = 'user', 'following'

        validators = [
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def create(self, validated_data):
        user = self.context.get('request').user
        following = validated_data.get('following')
        follow = Follow.objects.create(user=user, following=following)
        return follow

    def validate(self, data):
        if not data.get('following'):
            raise exceptions.ParseError(
                'Required field is missing or not valid.'
            )
        if data.get('following') == self.context.get('request').user:
            raise exceptions.ValidationError(
                "You can't subscribe to yourself."
            )
        return data
