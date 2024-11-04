from .models import Product, ProductImage, Rating, Cart, CartItem
from .serializers import (ProductSerializer,
                        ProductImageSerializer,
                        RatingSerializer,
                        CartSerializer,
                        CartItemSerializer
                        )
from ..users.models import Profile
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets, generics
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
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        cart = self.get_object()
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)
        if quantity < 1:
            return Response("Quantity can not be less than 1", status=400)
        
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
        
        return Response({'status': 'item added to cart'}, status=status.HTTP_200_OK)

    
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
    
    