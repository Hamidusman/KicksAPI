from django.contrib import admin
from .models import (Product, ProductImage,
                    Rating, ShoeSize, Color,
                    Cart, CartItem)
# Register your models here.
admin.site.register(ShoeSize)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(CartItem)
