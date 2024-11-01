from django.contrib import admin
from .models import Product, ProductImage, Rating, ShoeSize, Color
# Register your models here.
admin.site.register(ShoeSize)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Rating)
