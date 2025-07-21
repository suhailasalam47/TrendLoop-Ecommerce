from django.db import models

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    product_image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return self.product_name