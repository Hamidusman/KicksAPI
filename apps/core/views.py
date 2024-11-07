from .models import Product, ProductImage, Rating, Cart, CartItem
from .serializers import (ProductSerializer,
                        ProductImageSerializer,
                        RatingSerializer,
                        CartSerializer,
                        CartItemSerializer
                        )
from ..users.models import Profile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from .filters import ProductFilter

@method_decorator(cache_page(60*15), name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

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
        return Response({'message': 'Image Added Successfully'})


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        if quantity < 1:
            return Response({"message": "Quantity cannot be less than 1"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=404)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        cart_item.quantity += quantity
        cart_item.save()

        # Return response with cart item details
        return Response({
            'message': 'Product added to cart',
            'cart_item': CartItemSerializer(cart_item).data
        }, status=201)
        
    @action(detail=True, methods=['delete'], url_path='remove-item/(?P<item_id>\d+)')
    def remove_item(self, request, pk=None, item_id=None):
        try:
            cart = self.get_object()
            cart_item = CartItem.objects.get(cart=cart, id=item_id)
            cart_item.delete()
            return Response({'status': 'item removed from cart'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
    
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
    
    