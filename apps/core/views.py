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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response("Product Deleted Successfully")
    
    @action(detail=True, methods=['get'])
    def total_rating(self, request, *args, **kwargs):
        product = self.get_object()
        
        total_rating = Rating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
        return Response({
            'total_rating': total_rating or 0
        })
    

class ProductImagesView(generics.ListCreateAPIView):
    queryset = ProductImage
    serializer_class = ProductImageSerializer
    

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
    
    