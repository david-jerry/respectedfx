from respectedfx.blog.models import Post
from respectedfx.fxrates.models import ExchangeRates


def posts(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "latest_posts": Post.get_latest_posts()
    }
