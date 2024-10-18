from rest_framework import serializers
from .models import Product, ProductImage, Rating

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name','description',
            'price', 'category',
            'quantity', 'main_image',
            'uploaded_at'
        ]
        read_only_fields = ['uploaded_at']
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product', 'image']
        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['product', 'Rating']

