from rest_framework import serializers
from .models import Receipt, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['receipt']


class ReceiptSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = '__all__'

    def create(self, validated_data):
        items = validated_data.pop('items')
        receipt = Receipt.objects.create(**validated_data)
        for item in items:
            Item.objects.create(receipt=receipt, **item)
        return receipt


class ReceiptModelCreateSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id']


class ReceiptModelRetrieveSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['points']
