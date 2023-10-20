from django.db import models
from django.db.models import CharField, ManyToManyField, EmailField, OneToOneField, BooleanField, ImageField, CASCADE, ForeignKey, DO_NOTHING

from model_utils.models import TimeStampedModel

from respectedfx.newsletter.tasks import send_newsletter_mails

# Create your models here.
class ExchangeRates(TimeStampedModel):
    local_currency_name = CharField(max_length=10, default="NGN")
    local_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    foreign_currency_name = CharField(max_length=10, default="USD")
    foreign_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    active = BooleanField(default=True)

    def __str__(self):
        return f"{self.foreign_currency_name.upper()} - {self.local_currency_name.upper()}"

class LastRates(TimeStampedModel):
    rates = OneToOneField(ExchangeRates, on_delete=CASCADE, related_name="last_rates")
    local_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    foreign_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Previous Rates: {self.rates.foreign_currency_name.upper()} - {self.rates.local_currency_name.upper()}"

    @property
    def increased(self):
        if self.rates.local_amount > self.local_amount:
            return True
        return False

    @property
    def percentage_change(self):
        if self.local_amount != self.rates.local_amount:
            percentage_change = ((self.local_amount - self.rates.local_amount) / self.rates.local_amount) * 100
            if percentage_change > 0.0000:
                return f"{percentage_change:.4f}%"
            elif percentage_change < 0.0000:
                return f"{abs(percentage_change):.4f}%"
            else:
                return 0.0000
        else:
            return 0.0000

class TransferToBanks(TimeStampedModel):
    bank_name = CharField(max_length=250, default="Access Bank", unique=True)
    account_number = CharField(max_length=20, default="Access Bank", unique=True)
    account_name = CharField(max_length=250, default="John Doe", unique=True)


    def __str__(self):
        return self.bank_name

class FXRequest(TimeStampedModel):
    email = models.EmailField(max_length=300, null=True)
    bank = ForeignKey(TransferToBanks, on_delete=CASCADE, related_name="fxrequest")
    amount = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    currency = CharField(max_length=10)
    to_currency = CharField(max_length=10, default="NGN")
    account_number = CharField(max_length=20)
    account_name = CharField(max_length=200)

    def __str__(self):
        return f"FX Request {self.account_name} | {self.amount} | {self.bank}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the save method of the superclass
        attachment = None
        recipients_emails = ["info@respectedfx.com"]
        body = f"""A new request to exchange {self.amount}{self.currency.upper()} to {self.to_currency.upper()} has been made by {self.email}, please proceed and send an email back to them when this is complete."""

        # Call the Celery task to send emails to all recipients
        send_newsletter_mails.delay(recipients_emails, "New Exchange Request", body, attachment)


class FXTransferRequest(TimeStampedModel):
    email = models.EmailField(max_length=300, null=True)
    bank = ForeignKey(TransferToBanks, on_delete=CASCADE, related_name="fxtransfer")
    amount = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    currency = CharField(max_length=10)
    recipient_account_number = CharField(max_length=20)
    recipient_account_name = CharField(max_length=200)
    recipient_bank_code = CharField(max_length=15)

    def __str__(self):
        return f"International Transfer of {self.account_name} | {self.amount} | {self.bank}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the save method of the superclass
        attachment = None
        recipients_emails = ["info@respectedfx.com"]
        body = f"""A new request to transfer {self.amount}{self.currency.upper()} to {self.to_currency.upper()} has been made by {self.email}, please proceed and send an email back to them when this is complete."""

        # Call the Celery task to send emails to all recipients
        send_newsletter_mails.delay(recipients_emails, "International Transfer Request", body, attachment)


