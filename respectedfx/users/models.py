from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, OneToOneField, BooleanField, ImageField, CASCADE, ForeignKey, DO_NOTHING
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from respectedfx.newsletter.models import Newsletter

from respectedfx.users.managers import UserManager

from model_utils.models import TimeStampedModel
from django_countries.fields import CountryField

class User(AbstractUser):
    """
    Default custom user model for respectedfx.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def bank_accounts(self):
        if BankAccount.objects.filter(user=self).exists():
            return BankAccount.objects.filter(user=self)
        return []

    @property
    def receive_newsletter(self):
        if Newsletter.objects.filter(email=self.email).exists():
            if Newsletter.objects.filter(email=self.email, active=False).exists():
                return False
            elif Newsletter.objects.filter(email=self.email, active=True).exists():
                return True
        return False

    @property
    def receive_latest_blog(self):
        if Newsletter.objects.filter(email=self.email).exists():
            if Newsletter.objects.filter(email=self.email, active=False).exists():
                return False
            elif Newsletter.objects.filter(email=self.email, active=True, blog=True).exists():
                return True
        return False



    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Profile(TimeStampedModel):
    user = OneToOneField(User, verbose_name=_("User Profile"), on_delete=CASCADE, related_name="profile")
    phone = CharField(unique=False, max_length=17, blank=True, help_text=_("eg: 018276475673"))
    country = CountryField(blank_label="(select country)")
    photo = ImageField(upload_to='profile_pictures', null=True, blank=True)

    def __str__(self) -> str:
        return self.user.name + " Profile"

class KYC(TimeStampedModel):
    user = OneToOneField(User, verbose_name=_("User KYC"), on_delete=CASCADE, related_name="kyc")
    bvn = CharField(blank=True)
    verified = BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.name + " KYC"

class BankAccount(TimeStampedModel):
    user = ForeignKey(User, on_delete=CASCADE, related_name="bank_account")
    bank_name = CharField(max_length=250, default="Access Bank", unique=True)
    account_number = CharField(max_length=20, default="Access Bank", unique=True)
    account_name = CharField(max_length=250, default="John Doe", unique=True)

    def __str__(self):
        return f"{self.user.username} {self.bank_name}"
