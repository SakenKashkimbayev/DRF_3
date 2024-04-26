from django import forms
from rest_framework import serializers

from shop.models import Product, Category


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'end_registration_date']

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']