# blog/templatetags/blog_tags.py
from django import template
from blog.models import Post
from django.utils import timezone

register = template.Library()

@register.simple_tag
def latest_blog_posts(count=3):
    return Post.objects.filter(status=True, published_date__lte=timezone.now()).order_by('-published_date')[:count]
