from rest_framework import serializers
from .models import Post
from django.conf import settings

MAX_POST_LENGTH = settings.MAX_POST_LENGTH
POST_ACTION_OPTIONS = settings.POST_ACTION_OPTIONS


class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in POST_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action ")
        return value


class PostCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'likes']

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > MAX_POST_LENGTH:
            raise serializers.ValidationError("This post is too long!")
        return value


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    content = serializers.SerializerMethodField(read_only=True)
    parent = PostCreateSerializer( read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'likes', 'is_repost', 'parent']

    def get_likes(self, obj):
        return obj.likes.count()

    def get_content(self, obj):
        content = obj.content
        if obj.is_repost:
            content = obj.parent.content
        return content

