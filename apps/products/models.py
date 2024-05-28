import os
from datetime import datetime
from django.db import models
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=100, null=True, blank=False)

    def __str__(self):
        return self.name

# Hàm custom upload image brands path
def brand_image_upload_to(instance, filename):
    brand_slug = instance.slug
    now = datetime.now()
    return os.path.join('brands', brand_slug, str(now.year), str(now.month), str(now.day), filename)

class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=brand_image_upload_to, null=True, blank=True)

    def __str__(self):
        return self.name

    def product_count(self):
        return self.products.count()

# Hàm custom upload image products path
def product_image_upload_to(instance, filename):
    category_slug = instance.category.slug
    now = datetime.now()
    return os.path.join('products', category_slug, str(now.year), str(now.month), str(now.day), filename)

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=product_image_upload_to)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    top_selling = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    promotion = models.BooleanField(default=False)
    promotion_discount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def price_after_discount(self):
        if self.promotion and self.promotion_discount > 0:
            discount = self.promotion_discount / Decimal('100')
            return self.price * (Decimal('1') - discount)
        return self.price
