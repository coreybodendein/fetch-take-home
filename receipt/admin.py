from django.contrib import admin
from .models import Receipt


class ReceiptAdmin(admin.ModelAdmin):
    search_fields = ['id']


admin.site.register(Receipt, ReceiptAdmin)
