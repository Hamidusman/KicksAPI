from django.db.models import Avg
from rest_framework import serializers
from .models import Product, ProductImage, Rating

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
        
