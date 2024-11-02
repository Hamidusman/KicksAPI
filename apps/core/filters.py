from django_filters import rest_framework as filter
from .models import Product


class ProductFilter(filter.FilterSet):
    name = filter.CharFilter(lookup_expr='icontains')
    max_price = filter.NumberFilter(field_name='price', lookup_expr='lte')
    color = filter.CharFilter(field_name="colors__color", lookup_expr="icontains")
    shoe_size = filter.NumberFilter(field_name="shoe_size__size")
    
    class Meta:
        model = Product
        fields = ['category', 'max_price', 'name', 'color', 'shoe_size']