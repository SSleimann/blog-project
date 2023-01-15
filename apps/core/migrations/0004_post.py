# Generated by Django 4.1.5 on 2023-01-13 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_follower'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('title_slug', models.SlugField(verbose_name='slug')),
                ('content', models.TextField(max_length=250, verbose_name='content')),
                ('created_data', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
    ]
