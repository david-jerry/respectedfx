from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "respectedfx.blog"
    verbose_name = _("News")

    def ready(self):
        try:
            import respectedfx.blog.signals  # noqa: F401
        except ImportError:
            pass
