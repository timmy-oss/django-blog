# Generated by Django 3.2.5 on 2021-08-22 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpostcategory',
            options={'verbose_name_plural': 'Blog post categories'},
        ),
        migrations.AlterModelOptions(
            name='commentreply',
            options={'verbose_name_plural': 'Comment replies'},
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='tags',
            field=models.TextField(blank=True),
        ),
    ]