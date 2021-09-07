from django.contrib import admin

from .models import *

admin.site.register(BlogPost)
admin.site.register(BlogPostCategory)
admin.site.register(PostArticle)
admin.site.register(PostComment)
admin.site.register(PostImage)
admin.site.register(CommentReply)
