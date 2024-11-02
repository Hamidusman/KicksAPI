from django.db import models

from django.utils.translation import gettext_lazy as _
# Create your models here.

class ShoeSize(models.Model):
    size = models.IntegerField()

class Color(models.Model):
    color = models.CharField(max_length=20, unique=True)
    hex_code = models.CharField(max_length=9, unique=True)
    
    def __str__(self):
        return self.color
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=30)
    quantity = models.IntegerField()
    main_image = models.URLField(default=None, null=True,
                    verbose_name=_('main images'))
    uploaded_at = models.DateField(auto_now=True,
                    verbose_name=_('uploaded at'))
    
    colors = models.ManyToManyField(Color,
                    verbose_name=_('color Variants'))
    shoe_size = models.ManyToManyField(ShoeSize,
                    verbose_name=_('shoe sizes'))
    
    def __str__(self):
        return (self.name)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.URLField()
    
    def __str__(self):
        return (f'Images for {self.product}')

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    
    def __str__(self):
        return (f'Rating for {self.product}')