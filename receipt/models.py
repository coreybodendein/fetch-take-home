from datetime import time
from decimal import Decimal, ROUND_UP
import uuid
from django.db import models


class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    retailer = models.CharField(max_length=255)
    purchase_date = models.DateField()
    purchase_time = models.TimeField()
    total = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.id}: {self.points()}'

    def points(self):
        points = 0
        retailer = self.retailer
        points += sum(1 if char.isalpha() else 0 for char in retailer)
        total = Decimal(self.total)
        # mod 1 returns decimal part, if round number it's falsy, Decimal('0.00')
        if not total % Decimal('1'):
            points += 50
        if not total % Decimal('0.25'):
            points += 25
        items = self.items.all()
        points += 5 * (len(items) // 2)
        for item in items:
            description = item.short_description.strip()
            if not len(description) % 3:
                price = Decimal(item.price)
                item_points = price * Decimal('0.2')
                # round up to whole dollar
                item_points = item_points.quantize(Decimal('1.'), rounding=ROUND_UP)
                points += int(item_points)
        purchase_date = self.purchase_date
        if purchase_date.day % 2:
            points += 6
        purchase_time = self.purchase_time
        early_time = time(hour=14)  # 2pm
        late_time = time(hour=16)  # 4pm
        if early_time < purchase_time < late_time:
            points += 10
        return points


class Item(models.Model):
    receipt = models.ForeignKey(to=Receipt, on_delete=models.CASCADE, related_name='items')
    short_description = models.CharField(max_length=255)
    price = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.receipt_id}: {self.short_description}'
