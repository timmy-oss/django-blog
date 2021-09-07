from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify

from .models import BlogPost, BlogPostCategory


@receiver(post_save, sender=BlogPost, dispatch_uid='blog_post_signal_handler')
def blog_post_signal_handler(sender, **kwargs):
    instance = kwargs.get('instance')
    if not instance.slug_field:
        instance.slug_field = slugify(instance.title)
        instance.save()

    if instance.published and not(instance.pub_date):
        instance.pub_date = timezone.now()


@receiver(post_save, sender=BlogPostCategory, dispatch_uid='blog_post_category_signal_handler')
def blog_post_category_signal_handler(sender, **kwargs):
    instance = kwargs.get('instance')
    if not instance.slug_field:
        instance.slug_field = slugify(instance.title)
        instance.save()
