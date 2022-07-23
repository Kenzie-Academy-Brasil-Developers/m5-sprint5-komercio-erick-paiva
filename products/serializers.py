from django.forms import ValidationError
from rest_framework import serializers
from products.models import Product
from users.models import User


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "is_seller", "date_joined"]


class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "seller", "description", "price", "quantity", "is_active"]

    def create(self, validated_data):
        seller = validated_data.pop("seller")
        product = Product.objects.create(seller=seller, **validated_data)
        return product

    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError("the quantity must be a positive value !")
        return value

    def validate_price(self, price):
        if price < 0:
            raise ValidationError("The product price must be a positive value!")
        return price


class GetProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["description", "price", "quantity", "is_active", "seller_id"]
