# Generated by Django 4.1.5 on 2023-01-14 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_title_slug_post_slug_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='slug_title',
            new_name='title_slug',
        ),
    ]
