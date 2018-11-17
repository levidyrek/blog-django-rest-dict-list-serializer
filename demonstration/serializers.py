from django.db.models import Q
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from .models import Blog, BlogPost, Comment, User


class DictSerializer(serializers.ListSerializer):
    """
    Overrides default ListSerializer to return a dict with a custom field from
    each item as the key. Makes it easier to normalize the data so that there
    is minimal nesting. dict_key defaults to 'id' but can be overridden.
    """
    dict_key = 'id'

    @property
    def data(self):
        """
        Overriden to return a ReturnDict instead of a ReturnList.
        """
        ret = super(serializers.ListSerializer, self).data
        return ReturnDict(ret, serializer=self)

    def to_representation(self, data):
        """
        Converts the data from a list to a dictionary.
        """
        items = super(DictSerializer, self).to_representation(data)
        return {item[self.dict_key]: item for item in items}


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'username',)
        list_serializer_class = DictSerializer


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'author', 'comment', 'post')
        list_serializer_class = DictSerializer


class BlogPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        fields = ('id', 'author', 'body', 'comments', 'title',)
        list_serializer_class = DictSerializer


class BlogSerializer(serializers.ModelSerializer):
    posts = BlogPostSerializer(many=True)
    comments = serializers.SerializerMethodField()
    authors = serializers.SerializerMethodField()

    def get_comments(self, blog):
        comments = Comment.objects.filter(
            post__blog=blog,
        )
        return CommentSerializer(
            comments,
            many=True,
            context={'request': self.context['request']}
        ).data

    def get_authors(self, blog):
        comments = Comment.objects.filter(
            post__blog=blog,
        )
        authors = User.objects.filter(
            Q(comments__in=comments) | Q(posts__in=blog.posts.all()),
        )
        return UserSerializer(
            authors,
            many=True,
            context={'request': self.context['request']},
        ).data

    class Meta:
        model = Blog
        fields = ('id', 'authors', 'comments', 'name', 'posts',)
