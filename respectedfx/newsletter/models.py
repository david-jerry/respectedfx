from django.db import models
from django.db.models import CharField, ManyToManyField, EmailField, OneToOneField, BooleanField, ImageField, CASCADE, ForeignKey, DO_NOTHING
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField

from respectedfx.newsletter.tasks import send_newsletter_mails
from respectedfx.utils.logger import LOGGER

class Newsletter(TimeStampedModel):
    email = EmailField(_("Subscriber Email"), unique=True)
    active = BooleanField(default=True)
    blog = BooleanField(default=True)

    def __str__(self):
        return self.email


class NewsMail(TimeStampedModel):
    subject = CharField(max_length=250, blank=False, unique=True)
    recipients = ManyToManyField(Newsletter, verbose_name=_("Recipients"), related_name="mails")
    message = HTMLField()
    attachment = models.FileField(_(""), upload_to="newsletter", max_length=250)

    def __str__(self) -> str:
        return f"{self.subject} sent {self.created.date()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the save method of the superclass
        filepath = self.attachment.url
        filename = "attachment.pdf"

        recipients_emails = [subscriber.email for subscriber in self.recipients.filter(active=True)]
        LOGGER.info(recipients_emails)
        # Call the Celery task to send emails to all recipients
        send_newsletter_mails.delay(recipients_emails, self.subject, self.message, filepath, filename)

