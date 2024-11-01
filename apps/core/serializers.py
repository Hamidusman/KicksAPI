from rest_framework import serializers
from .models import Product, ProductImage, Rating

class ProductSerializer(serializers.ModelSerializer):
    colors = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='color'
    )
    shoe_size = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='size'
    )
    class Meta:
        model = Product
        fields = [
            'id',
            'name','description',
            'price', 'category',
            'quantity', 'main_image',
            'uploaded_at',
            'colors',
            'shoe_size'
        ]
        read_only_fields = ['uploaded_at']
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product', 'image']
        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['product', 'rating']

