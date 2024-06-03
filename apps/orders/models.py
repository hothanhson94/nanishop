from django.db import models
from django.contrib.auth.models import User
from apps.products.models import Product

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.product.name} ordered by {self.user.username}'