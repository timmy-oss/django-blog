# Generated by Django 3.2.5 on 2021-08-26 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20210823_0906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='likes',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='downvotes',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='upvotes',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
