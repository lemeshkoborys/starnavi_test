from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from starnavi_blog_api.models import Post, PostLikes
import starnavi_blog_api.serializers as post_serializers


class UserCreateAPIView(APIView):

    def post(self, request, format=None):
        serializer = post_serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.save():
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListCreateAPIView(ListCreateAPIView):

    queryset = Post.objects.all()
    serializer_class = post_serializers.PostModelSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostLikesAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, format=None):
        try:
            post = Post.objects.get(pk=request.data['post'])
        except Post.DoesNotExist:
            raise NotFound('Post does not exist')
        except ValueError:
            return Response(data={'error': 'Bad request.'}, status=status.HTTP_400_BAD_REQUEST)
        post_serializer = post_serializers.PostModelSerializer(post)
        try:
            postlike = PostLikes.objects.get(
                post=request.data['post'],
                user=self.request.user
            )

            postlike.delete()
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        except PostLikes.DoesNotExist:
            serializer = post_serializers.PostLikesModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response(post_serializer.data, status=status.HTTP_201_CREATED)

