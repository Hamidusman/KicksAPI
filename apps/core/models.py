from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=30)
    quantity = models.IntegerField()
    main_image = models.ImageField(upload_to='product-main-img/')
    uploaded_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return (self.name)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=('product-images/'))
    
    def __str__(self):
        return (f'Images for {self.product}')

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    
    def __str__(self):
        return (f'Rating for {self.product}')