# Generated by Django 4.1.3 on 2023-02-04 21:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0004_alter_post_author_alter_post_post_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_dislikes',
            field=models.ManyToManyField(related_name='post_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='post_likes',
            field=models.ManyToManyField(related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
