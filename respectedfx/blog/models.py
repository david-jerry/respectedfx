from django.db import models
from django.utils.text import slugify

from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField

from respectedfx.newsletter.tasks import send_newsletter_mails

# Create your models here.
class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(TimeStampedModel):
    URL = "URL"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    cover_photo = models.ImageField(upload_to='blog_posts', null=True, blank=True)
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='categories')
    tags = models.ManyToManyField(Tag, related_name='tags')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        attachment = {
            "filepath": self.cover_photo.url,
            "filename": f"{self.slug}.jpg"
        } if self.cover_photo.url else None
        recipients_emails = self.recipients.filter(active=True, blog=True).values_list('email', flat=True)

        # Call the Celery task to send emails to all recipients
        send_newsletter_mails.delay(recipients_emails, self.subject, self.message, attachment)


    @classmethod
    def get_latest_posts(cls, limit=6):
        return cls.objects.order_by('-created_at')[:limit] or []

    @property
    def get_related_posts(self, limit=3):
        return Post.objects.filter(tags__in=self.tags.all()).exclude(id=self.id).distinct()[:limit] or []
