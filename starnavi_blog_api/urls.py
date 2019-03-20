from django.urls import path
from starnavi_blog_api import views

urlpatterns = [
    path('posts/', views.PostListCreateAPIView.as_view(), name='posts'),
    path('posts/like/', views.PostLikesAPIView.as_view(), name='like-unlike'),
]
