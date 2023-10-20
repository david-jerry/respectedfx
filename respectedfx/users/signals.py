from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

from allauth.account.signals import user_signed_up, user_logged_in
from respectedfx.users.models import Profile

from respectedfx.utils.logger import LOGGER

User = get_user_model()

@receiver(post_save, sender=User)
def user_post_save_signal(created, instance, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
