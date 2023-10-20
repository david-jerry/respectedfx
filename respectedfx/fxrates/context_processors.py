from respectedfx.fxrates.models import ExchangeRates, TransferToBanks


def exchange_rates(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "rates": ExchangeRates.objects.filter(active=True) if ExchangeRates.objects.filter(active=True).exists() else None,
        "first_amount": ExchangeRates.objects.filter(active=True).first().local_amount  if ExchangeRates.objects.filter(active=True).exists() else None,
        "banks": TransferToBanks.objects.all()
    }
