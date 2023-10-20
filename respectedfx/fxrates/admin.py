from django.contrib import admin

from respectedfx.fxrates.models import ExchangeRates, LastRates, TransferToBanks, FXRequest, FXTransferRequest


# Register your models here.
admin.site.register(TransferToBanks)
admin.site.register(FXRequest)
admin.site.register(FXTransferRequest)

class OldRateInline(admin.StackedInline):
    model = LastRates
    can_delete = False
    verbose_name_plural = 'Old Rates'


@admin.register(ExchangeRates)
class ExchangeRatesAdmin(admin.ModelAdmin):
    inlines = [OldRateInline]
