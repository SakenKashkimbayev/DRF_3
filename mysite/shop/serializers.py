from django import forms
from rest_framework import serializers

from shop.models import Product, Category, Order, Warehouse


# , CartItem
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductSerializers(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    warehouse_data = serializers.IntegerField(read_only=True)
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category_id', 'category', 'warehouse_data']


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['pk', 'product', 'quantity', 'status_order']

class OrderDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'status_order']
# class WarehouseSerializers(serializers.ModelSerializer):
#     prod = ProductSerializers()
#
#     class Meta:
#         model = Warehouse
#         fields = ['total_quantity', 'prod']