from django.db import models
from django.contrib.auth.models import User


class PostLikes(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='User that have submitted like'
    )

    post = models.ForeignKey(
        'starnavi_blog_api.Post',
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Post that has been liked'
    )

    def __unicode__(self):
        return f'User: {self.user.username} has liked {self.post.title}'

    class Meta:
        db_table = 'likes'
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        # unique_together = ('user', 'post')


class Post(models.Model):

    title = models.CharField(
        max_length=225,
        verbose_name='Post title'
    )

    content = models.TextField(verbose_name='Post content')

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        editable=False,
        verbose_name='Post Author'
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date and Time Created'
    )

    def __unicode__(self):
        return self.title

    def get_likes_count(self):
        return PostLikes.objects.filter(post=self).count()

    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


