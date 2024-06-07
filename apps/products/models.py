import os
from datetime import datetime
from django.db import models
from decimal import Decimal
from django.urls import reverse
from apps.customers.models import Customer
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=100, null=True, blank=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category_detail', kwargs={'category_slug': self.slug})

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

def product_image_upload_to(instance, filename):
    category_slug = instance.category.slug
    now = datetime.now()
    return os.path.join('products', category_slug, str(now.year), str(now.month), str(now.day), filename)

def product_additional_image_upload_to(instance, filename):
    category_slug = instance.product.category.slug
    now = datetime.now()
    return os.path.join('products', category_slug, str(now.year), str(now.month), str(now.day), filename)

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = CKEditor5Field('Description', config_name='default')
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
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def price_after_discount(self):
        if self.promotion and self.promotion_discount > 0:
            discount = self.promotion_discount / Decimal('100')
            return self.price * (Decimal('1') - discount)
        return self.price

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum([review.rating for review in reviews]) / len(reviews)
        return 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    product_images = models.ImageField(upload_to=product_additional_image_upload_to, null=True, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"

class Feature(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='features', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, related_name='product_features', on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, related_name='product_features', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.feature.name}"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    review_text = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.product.name} by {self.customer.user.username}'
