from rest_framework import serializers
from .models import User, Vendor, Product, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id','username','email','role','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        pwd = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(pwd)
        return user.save() or user

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Vendor
        fields = ['id','name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ['id','name','price','image','created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OrderItem
        fields = ['product','quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    class Meta:
        model  = Order
        fields = ['id','items','created_at']

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = Order.objects.create(customer=self.context['request'].user)
        for it in items:
            OrderItem.objects.create(order=order, **it)
        return order
