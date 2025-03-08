from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='sub_categories')
    is_sub = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = 'Categories'
    

class Product(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='products')
    image = models.ImageField(upload_to='product_images/%Y/%m/%D')
    price = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ('-created_at',)
