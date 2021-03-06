# Generated by Django 2.1.7 on 2019-03-19 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('starnavi_blog_api', '0004_post_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AlterField(
            model_name='postlikes',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='starnavi_blog_api.Post', verbose_name='Post that has been liked'),
        ),
        migrations.AlterField(
            model_name='postlikes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='User that have submitted like'),
        ),
    ]
