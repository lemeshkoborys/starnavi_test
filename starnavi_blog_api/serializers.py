import requests
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from starnavi_blog_api.models import Post, PostLikes


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Email is already taken.'
        )]
    )

    username = serializers.CharField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Username is already taken.'
        )]
    )

    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user

    def validate(self, attrs):
        url = settings.EMAIL_TO_FIND_URL.format(attrs['email'])
        request = requests.get(url).json()
        if request['data']['gibberish'] or not request['data']['webmail']:
            raise ValidationError('Email is not valid or it does not exist')
        return attrs

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password'
        )


class PostModelSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return obj.get_likes_count()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'user',
            'likes',
            'created',
        )


class PostLikesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLikes
        fields = (
            'id',
            'post',
        )
