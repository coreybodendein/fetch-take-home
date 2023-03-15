from django.contrib import admin
from .models import Receipt, Item


class ReceiptAdmin(admin.ModelAdmin):
    search_fields = ['id']


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['receipt__id']


admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Item, ItemAdmin)
