from datetime import time
from decimal import Decimal, ROUND_UP
from rest_framework import serializers
from .models import Receipt


class ItemSerializer(serializers.Serializer):
    shortDescription = serializers.RegexField(regex=r'^[\w\s\-]+$')
    price = serializers.RegexField(regex=r'^\d+\.\d{2}$')


class ReceiptSerializer(serializers.Serializer):
    retailer = serializers.RegexField(regex=r'^\S+$')
    purchaseDate = serializers.DateField()
    purchaseTime = serializers.TimeField()
    items = ItemSerializer(many=True)
    total = serializers.RegexField(regex=r'^\d+\.\d{2}$')

    def validate_items(self, attrs):
        if len(attrs) == 0:
            raise serializers.ValidationError('at least one item is required')
        return attrs

    def create(self, validated_data):
        points = 0
        retailer = validated_data['retailer']
        points += sum(1 if char.isalpha() else 0 for char in retailer)
        total = Decimal(validated_data['total'])
        # mod 1 returns decimal part, if round number it's falsy, Decimal('0.00')
        if not total % Decimal('1'):
            points += 50
        if not total % Decimal('0.25'):
            points += 25
        items = validated_data['items']
        points += 5 * (len(items) // 2)
        for item in items:
            description = item['shortDescription'].strip()
            if not len(description) % 3:
                price = Decimal(item['price'])
                item_points = price * Decimal('0.2')
                # round up to whole dollar
                item_points = item_points.quantize(Decimal('1.'), rounding=ROUND_UP)
                points += int(item_points)
        purchase_date = validated_data['purchaseDate']
        if purchase_date.day % 2:
            points += 6
        purchase_time = validated_data['purchaseTime']
        early_time = time(hour=14)  # 2pm
        late_time = time(hour=16)  # 4pm
        if early_time < purchase_time < late_time:
            points += 10
        return Receipt.objects.create(points=points)


class ReceiptModelCreateSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id']


class ReceiptModelRetrieveSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['points']
