from datetime import time
from decimal import Decimal, ROUND_UP
import uuid
from django.db import models


class Receipt(models.Model):
    """Model representing a receipt"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    retailer = models.CharField(max_length=255)
    purchase_date = models.DateField()
    purchase_time = models.TimeField()
    total = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.id}: {self.points()}'

    def points(self):
        """Compute the points on this receipt"""
        points = 0

        # One point for every alphanumeric character in the retailer name.
        retailer = self.retailer
        points += sum(1 if char.isalpha() else 0 for char in retailer)

        # 50 points if the total is a round dollar amount with no cents.
        total = Decimal(self.total)
        # mod 1 returns decimal part, if round number it's falsy, Decimal('0.00')
        if not total % Decimal('1'):
            points += 50

        # 25 points if the total is a multiple of `0.25`.
        if not total % Decimal('0.25'):
            points += 25

        # 5 points for every two items on the receipt.
        items = self.items.all()
        points += 5 * (len(items) // 2)

        # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to
        # the nearest integer. The result is the number of points earned.
        for item in items:
            description = item.short_description.strip()
            if not len(description) % 3:
                price = Decimal(item.price)
                item_points = price * Decimal('0.2')
                # round up to whole dollar
                item_points = item_points.quantize(Decimal('1.'), rounding=ROUND_UP)
                points += int(item_points)

        # 6 points if the day in the purchase date is odd.
        purchase_date = self.purchase_date
        if purchase_date.day % 2:
            points += 6

        # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        purchase_time = self.purchase_time
        early_time = time(hour=14)  # 2pm
        late_time = time(hour=16)  # 4pm
        if early_time < purchase_time < late_time:
            points += 10

        return points


class Item(models.Model):
    """Model representing a receipt item"""
    receipt = models.ForeignKey(to=Receipt, on_delete=models.CASCADE, related_name='items')
    short_description = models.CharField(max_length=255)
    price = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.receipt_id}: {self.short_description}'
