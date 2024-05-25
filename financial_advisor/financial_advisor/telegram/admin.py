from django.contrib import admin

from financial_advisor.telegram.models import TelegramMessage

# Register your models here.
admin.site.register(TelegramMessage)
