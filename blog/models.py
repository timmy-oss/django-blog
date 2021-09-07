import random

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone


# INFO  BlogPostCategory
class BlogPostCategory(models.Model):
    title = models.CharField(max_length=120, unique=True)
    tags = models.TextField()
    slug_field = models.SlugField(
        null=True, max_length=128, unique=True, editable=False)

    class Meta:
        verbose_name_plural = 'Blog post categories'

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slugname': self.slug_field})

    def __str__(self):
        return self.title


# INFO BlogPost Model
class BlogPost(models.Model):
    title = models.CharField(max_length=128)
    drafted = models.DateTimeField(auto_now_add=True)
    slug_field = models.SlugField(
        max_length=128, unique=True, editable=False, null=True)
    published = models.BooleanField(default=False)
    pub_date = models.DateTimeField(null=True, editable=False)
    tags = models.TextField(blank=True)
    author = models.ForeignKey(get_user_model(
    ), related_name='authored_posts', on_delete=models.SET_NULL, null=True)
    upvotes = models.PositiveBigIntegerField(default=0)
    downvotes = models.PositiveBigIntegerField(default=0)
    category = models.ForeignKey(
        BlogPostCategory, related_name='posts', on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(null=True)
    layout = models.PositiveSmallIntegerField(default=0)

    def get_parts(self):
        articles = self.articles.all()
        images = self.imgs.all()
        parts = list(articles) + list(images)
        def func(next): return next.layout_id
        sorted_parts = sorted(parts, key=func)
        return sorted_parts

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'slugname': self.slug_field})

    def get_intro_text(self):
        if self.articles.count() == 0:
            return ''
        return self.articles.all()[0].content[:128]

    def get_mock_cover(self):
        temp = random.randint(1, 7)
        return '/static/blog/img/pic{0}.jpg'.format(temp)

    def get_pub_date(self):
        if not self.pub_date:
            return timezone.now()

    def __str__(self) -> str:
        return self.title


# INFO PostArticle
class PostArticle(models.Model):
    heading = models.CharField(max_length=128, null=True, blank=True)
    content = models.TextField(blank=False)
    published = models.BooleanField(default=False)
    layout_id = models.PositiveSmallIntegerField(null=True)
    post = models.ForeignKey(
        BlogPost, related_name='articles', on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:64]

    def is_article(self):
        return True

    def is_image(self):
        return False


# INFO PostImage


class PostImage(models.Model):
    caption = models.CharField(max_length=64)
    file = models.ImageField(blank=True, null=True)
    layout_id = models.PositiveSmallIntegerField(null=True)
    post = models.ForeignKey(
        BlogPost, related_name='imgs', on_delete=models.CASCADE)

    def __str__(self):
        return 'IMG {0}'.format(self.id)

    def is_article(self):
        return False

    def is_image(self):
        return True

# INFO PostComment


class PostComment(models.Model):
    post = models.ForeignKey(
        BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        get_user_model(), related_name='authored_comments', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1024)
    likes = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['-pub_date', ]

    def __str__(self):
        return "COMMENT {0}".format(self.id)


# INFO CommentReply
class CommentReply(models.Model):
    comment = models.ForeignKey(
        PostComment, related_name='replies', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(), related_name='authored_replies', on_delete=models.CASCADE)
    content = models.CharField(max_length=512)

    class Meta:
        verbose_name_plural = 'Comment replies'

    def __str__(self):
        return 'REPLY {0}'.format(self.id)
