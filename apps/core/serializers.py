from django.db.models import Avg
from rest_framework import serializers
from .models import (Product, ProductImage,
                    Rating, Cart, CartItem,
                    Transaction, TransactionItem,
                    )

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['product', 'rating']

class ProductSerializer(serializers.ModelSerializer):
    average_ratings = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id',
            'name', 'description',
            'price', 'category',
            'quantity', 'main_image',
            'uploaded_at',
            'colors',
            'shoe_size',
            'average_ratings'
        ]
        read_only_fields = ['uploaded_at', 'average_rating']

    def get_average_ratings(self, obj):
        average_rating = Rating.objects.filter(product=obj).aggregate(Avg('rating'))['rating__avg']
        return round(average_rating, 1) if average_rating is not None else 0.0
        
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product', 'image']
        

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id','product', 'quantity']
    
class CartSerializer(serializers.ModelSerializer):
    item = CartItemSerializer(many=True, required=False)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'item']
        read_only_fields = ['user']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        cart = Cart.objects.create(**validated_data)
        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)
        return cart