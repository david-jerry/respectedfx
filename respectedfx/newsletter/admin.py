from django.contrib import admin
from .models import (
    Newsletter,
    NewsMail
)
# Register your models here.
admin.site.register(Newsletter)
admin.site.register(NewsMail)
