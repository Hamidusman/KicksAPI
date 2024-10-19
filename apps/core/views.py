from .models import Product, ProductImage, Rating
from .serializers import (ProductSerializer,
                        ProductImageSerializer,
                        RatingSerializer,
                        )
from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, generics
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'])
    def average_rating(self, request, *args, **kwargs):
        product = self.get_object()
        average_rating = Rating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
        return Response({'average_rating': average_rating or 0})

    @action(detail=True, methods=['post'])
    def add_product_image(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ProductImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response({'message': 'Image Added Successfully'}, status=status.HTTP_201_CREATED)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = serializer.validated_data.get('rating')
        
        # ensures the rating are between 1 to 5
        if rating < 1 or rating > 5:
            return Response('error: Ratings are only between 1 to 5', status=400)
        serializer.save()
        return Response(serializer.data)
    
    