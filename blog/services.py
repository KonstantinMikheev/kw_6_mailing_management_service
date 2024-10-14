from django.conf import settings
from django.core.cache import cache

from blog.models import Blog


def get_posts_from_cache():
    """
    Get post from cache. If cache is disabled, retrieve from database.
    Returns:
        Post: The latest post from the database or from cache.
    """
    if not settings.CACHE_ENABLED:
        posts = Blog.objects.all()
    else:
        key = 'posts'
        posts = cache.get(key)
        if posts is None:
            posts = Blog.objects.all()
            cache.set(key, posts)

    return posts