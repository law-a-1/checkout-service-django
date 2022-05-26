from django.db import models

# Create your models here.

class Cart(models.Model):
    username = models.CharField(max_length=255, unique=True)
    grand_total = models.IntegerField(default=0)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    images = models.CharField(max_length=255)
    video = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class Item(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)

    product = models.ForeignKey(Product, related_name="product", on_delete=models.CASCADE)
    amount = models.IntegerField()
    total_price = models.IntegerField()