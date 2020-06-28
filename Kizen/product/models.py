from django.db import models


class Product(models.Model):
    """
    class to mmap to database the product model
    """

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True)
    image = models.ImageField(null=True, upload_to='products/%Y%m%d%H%M%S/')
    price = models.FloatField(default=0.0, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
