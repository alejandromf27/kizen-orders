from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Order(models.Model):
    """
    the order model
    """

    number = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.number).zfill(5)

    def get_total_price(self):
        return sum([line.subtotal_price for line in self.lines.all()])

    def save(self, *args, ** kwargs):
        self.total_price = self.get_total_price()
        super(Order, self).save(*args, **kwargs)


class OrderLine(models.Model):
    """
    model that represent lines of the order by each product
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.order.__str__() + ' / ' + self.product.name

    def get_subtotal_price(self):
        return self.quantity * self.product.price

    def save(self, *args, ** kwargs):
        self.subtotal_price = self.get_subtotal_price()
        super(OrderLine, self).save(*args, **kwargs)
