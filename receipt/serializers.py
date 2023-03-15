from rest_framework import serializers
from .models import Receipt, Item


class ItemSerializer(serializers.ModelSerializer):
    """Receipt item part of the serializer"""
    class Meta:
        model = Item
        exclude = ['receipt']


class ReceiptSerializer(serializers.ModelSerializer):
    """Main receipt serializer"""
    items = ItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = '__all__'

    def create(self, validated_data):
        # need to create the related receipt items manually
        items = validated_data.pop('items')
        receipt = Receipt.objects.create(**validated_data)
        for item in items:
            Item.objects.create(receipt=receipt, **item)
        return receipt


class ReceiptModelCreateSerialzier(serializers.ModelSerializer):
    """Serializer for the create response"""
    class Meta:
        model = Receipt
        fields = ['id']


class ReceiptModelRetrieveSerialzier(serializers.ModelSerializer):
    """Serializer for the retrieve response"""
    class Meta:
        model = Receipt
        fields = ['points']
